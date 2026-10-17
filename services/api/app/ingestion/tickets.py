"""Human-confirmed status edits retain all other source claims and revision history."""

import json
from pathlib import Path
from fastapi import HTTPException
from app.config import settings
from app.domain.models import Candidate, SourceEnvelope, now_iso


def ticket_snapshot(repo, source_id):
    source = repo.source(source_id)
    if not source or source["kind"] != "ticket":
        raise HTTPException(404, "This record is unavailable")
    revision = next(r for r in repo.revisions(source_id) if r["id"] == source["active_revision_id"])
    rows = repo.query(
        """MATCH (r:SourceRevision {id:$revision})-[:HAS_CHUNK]->(ch:Chunk)
        MATCH (c:Claim)-[p:SUPPORTED_BY]->(ch) MATCH (c)-[:SUBJECT]->(e:Entity)
        OPTIONAL MATCH (c)-[:OBJECT]->(o:Entity)
        RETURN c,e.id,e.kind,o.id,ch.char_start,p.start,p.end""",
        {"revision": revision["id"]},
    )
    tickets = {row[1] for row in rows if row[2] == "Ticket"}
    if len(tickets) != 1:
        raise HTTPException(409, "This source needs a single ticket. Update the source file instead.")
    entity_id = next(iter(tickets))
    return source, revision, rows, entity_id


def details(repo, source_id):
    source, revision, rows, entity_id = ticket_snapshot(repo, source_id)
    claims, _ = repo.claims([source_id])
    values = {c.scalar for c in claims if c.subject_id == entity_id and c.predicate == "STATUS"}
    return dict(
        source_id=source_id,
        entity_id=entity_id,
        title=revision["title"],
        expected_revision_id=revision["id"],
        status=next(iter(values)) if len(values) == 1 else None,
        blocked_entities=sorted(
            {c.object_id for c in claims if c.subject_id == entity_id and c.predicate == "BLOCKS"}
        ),
    )


def prepare_update(repo, source_id, expected_revision_id, status):
    source, revision, rows, entity_id = ticket_snapshot(repo, source_id)
    if revision["id"] != expected_revision_id:
        raise HTTPException(409, "This ticket changed. Reopen it before saving.")
    path = (Path(settings.upload_dir) / revision["content_path"]).resolve()
    if not path.is_relative_to(Path(settings.upload_dir).resolve()) or not path.is_file():
        raise HTTPException(409, "Original source is unavailable. Reimport it before updating.")
    body = path.read_text()
    previous_statuses = []
    retained = []
    for node, subject, kind, obj, chunk_start, start, end in rows:
        c = node.properties
        a, b = chunk_start + start, chunk_start + end
        if c["predicate"] == "STATUS" and subject == entity_id:
            previous_statuses.append((a, b))
            continue
        retained.append(
            dict(
                subject_id=subject,
                predicate=c["predicate"],
                object_id=obj,
                scalar=json.loads(c["scalar_json"]),
                quote=body[a:b],
                scope=c["scope"],
                extraction_score=c["extraction_score"],
                valid_from_ms=c.get("valid_from_ms"),
                valid_to_ms=c.get("valid_to_ms"),
                _span=(a, b),
            )
        )
    # If a quotation combines the status and other facts, editing it would alter evidence.
    if any(a < d and c < b for a, b in previous_statuses for c, d in [x["_span"] for x in retained]):
        raise HTTPException(
            409, "The status shares a passage with other facts. Update the source file instead."
        )
    for a, b in sorted(previous_statuses, reverse=True):
        body = body[:a] + body[b:]
    body = body + "\n\n"
    label = next(e[0] for e in repo.query("MATCH (e:Entity {id:$id}) RETURN e.label", {"id": entity_id}))
    quote = f"{label} has status {status}."
    new_start = len(body)
    body += quote
    candidates = []
    for c in retained:
        a, b = c.pop("_span")
        shift = sum(end - start for start, end in previous_statuses if end <= a)
        candidates.append(Candidate(**c, start=a - shift, end=b - shift))
    candidates.append(
        Candidate(
            subject_id=entity_id,
            predicate="STATUS",
            scalar=status,
            quote=quote,
            start=new_start,
            end=len(body),
        )
    )
    envelope = SourceEnvelope(
        source_id=source_id,
        kind="ticket",
        title=revision["title"],
        source_updated_at=now_iso(),
        acl_groups=source["acl_groups"],
        body=body,
        expected_revision_id=revision["id"],
    )
    return envelope, candidates
