"""Reviewed read-only tools. A model selects names/IDs, never executable graph queries."""

import time
from typing import Literal
from pydantic import Field, model_validator
from app.domain.models import Strict, Claim, Entity
from app.ingestion.service import registry

ToolName = Literal[
    "resolve_entity",
    "search_evidence",
    "get_project_context",
    "trace_dependencies",
    "find_blockers",
    "find_ownership",
]


class ToolArguments(Strict):
    entity_id: str | None = None
    entity_ids: list[str] | None = Field(default=None, max_length=20)
    name: str | None = Field(default=None, max_length=200)
    query: str | None = Field(default=None, max_length=2000)
    direction: Literal["forward", "reverse"] | None = None
    max_business_hops: int | None = Field(default=None, ge=0, le=3)


class ToolCall(Strict):
    name: ToolName
    arguments: ToolArguments

    @model_validator(mode="after")
    def allowed_arguments(self):
        supplied = {k for k, v in self.arguments.model_dump().items() if v is not None}
        allowed = {
            "resolve_entity": ({"name"}, {"name"}),
            "search_evidence": ({"query"}, {"query", "entity_ids"}),
            "get_project_context": ({"entity_id"}, {"entity_id"}),
            "trace_dependencies": ({"entity_id"}, {"entity_id", "direction", "max_business_hops"}),
            "find_blockers": ({"entity_ids"}, {"entity_ids"}),
            "find_ownership": ({"entity_id"}, {"entity_id"}),
        }
        required, permitted = allowed[self.name]
        if not required <= supplied or not supplied <= permitted:
            raise ValueError("Arguments are incompatible with the selected tool")
        return self


class ToolDecision(Strict):
    calls: list[ToolCall] = Field(default_factory=list, max_length=3)
    finish: bool = False


class ToolTrace(Strict):
    tool: ToolName
    round: int
    claim_count: int
    duration_ms: int


class ToolResult(Strict):
    tool: ToolName
    entity_ids: list[str]
    claims: list[Claim]
    truncated: bool = False


class KnowledgeChanged(Exception):
    pass


class ReadTools:
    def __init__(self, repo, groups: list[str], epoch: int, root: Entity):
        self.repo, self.groups, self.epoch = repo, groups, epoch
        self.directory = {e["id"]: Entity.model_validate(e) for e in registry()}
        self.observed = {root.id}
        self.trace: list[ToolTrace] = []
        self.results: list[ToolResult] = []
        self.calls: list[ToolCall] = []

    def execute(self, call: ToolCall, round_number: int) -> ToolResult:
        if len(self.trace) >= 6 or round_number > 2:
            raise ValueError("Agent tool budget exceeded")
        args = call.arguments
        ids = set(args.entity_ids or []) | ({args.entity_id} if args.entity_id else set())
        if not ids <= self.observed:
            raise ValueError("A tool can expand only entities observed in this investigation")
        started = time.monotonic()
        with self.repo.lock:
            if self.repo.epoch() != self.epoch:
                raise KnowledgeChanged()
            sources = self.repo.sources(self.groups)
            if call.name == "resolve_entity":
                matches = [
                    e.id
                    for e in self.directory.values()
                    if args.name.lower() in [e.label.lower(), *[a.lower() for a in e.aliases]]
                ]
                rows = self.repo.query("MATCH (e:Entity) WHERE e.id IN $ids RETURN e.id", {"ids": matches})
                result = ToolResult(tool=call.name, entity_ids=[r[0] for r in rows], claims=[])
            else:
                claims, truncated = self.repo.claims([s["id"] for s in sources])
                chosen = self._select(call, claims)
                entities = set(ids)
                for c in chosen:
                    entities.add(c.subject_id)
                    if c.object_id:
                        entities.add(c.object_id)
                result = ToolResult(
                    tool=call.name,
                    entity_ids=sorted(entities),
                    claims=chosen[:150],
                    truncated=truncated or len(chosen) > 150,
                )
        self.observed.update(result.entity_ids)
        self.results.append(result)
        self.calls.append(call)
        self.trace.append(
            ToolTrace(
                tool=call.name,
                round=round_number,
                claim_count=len(result.claims),
                duration_ms=round((time.monotonic() - started) * 1000),
            )
        )
        return result

    def _select(self, call: ToolCall, claims: list[Claim]) -> list[Claim]:
        args = call.arguments
        if call.name == "get_project_context":
            if self.directory[args.entity_id].kind != "Project":
                raise ValueError("Project context requires a project")
            commitments = {
                c.subject_id for c in claims if c.predicate == "REQUIRES" and c.object_id == args.entity_id
            }
            return [
                c
                for c in claims
                if (c.subject_id == args.entity_id and c.predicate == "USES")
                or (c.subject_id in commitments and c.predicate in {"REQUIRES", "MADE_TO", "DUE_ON"})
                or (c.predicate == "ABOUT" and c.object_id == args.entity_id)
            ]
        if call.name == "find_ownership":
            return [
                c
                for c in claims
                if (c.subject_id == args.entity_id and c.predicate == "OWNED_BY")
                or (c.object_id == args.entity_id and c.predicate == "WORKED_ON")
            ]
        if call.name == "find_blockers":
            blockers = [c for c in claims if c.predicate == "BLOCKS" and c.object_id in args.entity_ids]
            tickets = {c.subject_id for c in blockers}
            return blockers + [c for c in claims if c.subject_id in tickets and c.predicate == "STATUS"]
        if call.name == "search_evidence":
            candidates = [
                c
                for c in claims
                if not args.entity_ids or c.subject_id in args.entity_ids or c.object_id in args.entity_ids
            ]
            import re

            terms = {t for t in re.findall(r"[a-z0-9]+", args.query.lower()) if len(t) > 2}
            ranked = sorted(
                candidates,
                key=lambda c: len(terms.intersection(re.findall(r"[a-z0-9]+", c.evidence.quote.lower()))),
                reverse=True,
            )
            return ranked[:150]
        if call.name == "trace_dependencies":
            related = [
                c
                for c in claims
                if c.predicate in {"USES", "DEPENDS_ON", "BLOCKS", "REQUIRES"} and c.object_id
            ]
            reached = {args.entity_id}
            chosen = {}
            queue = [(args.entity_id, 0)]
            best = {args.entity_id: 0}
            max_hops = args.max_business_hops if args.max_business_hops is not None else 3
            while queue:
                current, hops = queue.pop(0)
                for c in related:
                    if args.direction == "reverse":
                        match = c.object_id == current
                        neighbor = c.subject_id
                    else:
                        match = c.subject_id == current and c.predicate in {"USES", "DEPENDS_ON"}
                        neighbor = c.object_id
                        if (
                            self.directory[args.entity_id].kind == "Ticket"
                            and c.subject_id == current
                            and c.predicate == "BLOCKS"
                        ):
                            match = True
                    distance = hops + int(c.predicate == "DEPENDS_ON")
                    if match and distance <= max_hops:
                        chosen[c.id] = c
                        reached.add(neighbor)
                        if neighbor not in best or distance < best[neighbor]:
                            best[neighbor] = distance
                            queue.append((neighbor, distance))
            # Reverse paths establish project context and preserve every intermediate source.
            projects = {id for id in reached if self.directory[id].kind == "Project"}
            commitments = {
                c.subject_id for c in claims if c.predicate == "REQUIRES" and c.object_id in projects
            }
            for c in claims:
                if (
                    c.subject_id in commitments
                    and c.predicate in {"REQUIRES", "MADE_TO", "DUE_ON"}
                    or c.predicate == "ABOUT"
                    and c.object_id in projects
                ):
                    chosen[c.id] = c
            return list(chosen.values())
        raise ValueError("Unsupported read tool")

    def observations(self) -> list[dict]:
        # The next model step sees only permitted tool results, bounded to 16 source passages.
        result = []
        seen_evidence = set()
        for r in self.results:
            visible = []
            for c in r.claims:
                if c.evidence.id not in seen_evidence and len(seen_evidence) >= 16:
                    continue
                seen_evidence.add(c.evidence.id)
                visible.append(
                    {
                        "subject_id": c.subject_id,
                        "predicate": c.predicate,
                        "object_id": c.object_id,
                        "scalar": c.scalar,
                        "evidence_id": c.evidence.id,
                        "quote": c.evidence.quote,
                    }
                )
            result.append(
                {"tool": r.tool, "entity_ids": r.entity_ids, "claims": visible, "truncated": r.truncated}
            )
        return result
