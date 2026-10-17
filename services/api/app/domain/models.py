from datetime import datetime, date, timezone
from enum import StrEnum
from hashlib import sha256
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_serialization_defaults_required=True)


def uid(prefix: str, *parts: object) -> str:
    return prefix + "_" + sha256("|".join(map(str, parts)).encode()).hexdigest()[:24]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ms(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)


def iso(value: int) -> str:
    return datetime.fromtimestamp(value / 1000, timezone.utc).isoformat()


class Kind(StrEnum):
    Person = "Person"
    Team = "Team"
    Project = "Project"
    Service = "Service"
    Customer = "Customer"
    Ticket = "Ticket"
    Decision = "Decision"
    Commitment = "Commitment"


class Entity(Strict):
    id: str
    kind: Kind
    label: str
    aliases: list[str] = Field(default_factory=list)


PREDICATES = {
    "USES": ({"Project"}, {"Service"}),
    "DEPENDS_ON": ({"Service"}, {"Service"}),
    "BLOCKS": ({"Ticket"}, {"Service", "Project"}),
    "REQUIRES": ({"Commitment"}, {"Project"}),
    "MADE_TO": ({"Commitment"}, {"Customer"}),
    "OWNED_BY": ({"Service", "Project"}, {"Person", "Team"}),
    "MEMBER_OF": ({"Person"}, {"Team"}),
    "WORKED_ON": ({"Person"}, {"Service", "Project", "Ticket"}),
    "ABOUT": ({"Decision"}, {"Project", "Service"}),
    "STATUS": ({"Ticket"}, set()),
    "DUE_ON": ({"Commitment"}, set()),
}


class Candidate(Strict):
    subject_id: str
    predicate: Literal[
        "USES",
        "DEPENDS_ON",
        "BLOCKS",
        "REQUIRES",
        "MADE_TO",
        "OWNED_BY",
        "MEMBER_OF",
        "WORKED_ON",
        "ABOUT",
        "STATUS",
        "DUE_ON",
    ]
    object_id: str | None = None
    scalar: str | None = None
    scope: str = "primary"
    quote: str = Field(min_length=1, max_length=1500)
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    extraction_score: float = Field(default=1.0, ge=0, le=1)
    valid_from_ms: int | None = None
    valid_to_ms: int | None = None

    @model_validator(mode="after")
    def shape(self):
        if (self.object_id is None) == (self.scalar is None):
            raise ValueError("Exactly one object or scalar is required")
        if self.end <= self.start:
            raise ValueError("Invalid evidence span")
        if self.predicate == "STATUS" and self.scalar not in {
            "open",
            "in_progress",
            "blocked",
            "done",
            "cancelled",
        }:
            raise ValueError("Invalid ticket status")
        if self.predicate == "DUE_ON":
            date.fromisoformat(self.scalar or "")
        if (
            self.valid_from_ms is not None
            and self.valid_to_ms is not None
            and self.valid_from_ms >= self.valid_to_ms
        ):
            raise ValueError("Validity interval must be increasing")
        return self


class TicketRecord(Strict):
    entity_id: str
    status: Literal["open", "in_progress", "blocked", "done", "cancelled"] | None = None
    blocks: list[str] = Field(default_factory=list, max_length=10)


class SourceEnvelope(Strict):
    schema_version: Literal["1.0"] = "1.0"
    source_id: str = Field(min_length=1, max_length=150, pattern=r"^[a-zA-Z0-9:_-]+$")
    kind: Literal["directory", "document", "chat", "ticket", "decision"]
    title: str = Field(min_length=1, max_length=200)
    source_updated_at: str
    acl_groups: list[Literal["all_employees", "engineering", "leadership"]] = Field(max_length=3)
    body: str = Field(max_length=100000)
    records: TicketRecord | None = None
    expected_revision_id: str | None = None
    external_url: None = None

    @field_validator("source_updated_at")
    @classmethod
    def timestamp(cls, value: str) -> str:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Timestamp must include timezone")
        return parsed.astimezone(timezone.utc).isoformat()


class Extraction(Strict):
    claims: list[Candidate] = Field(default_factory=list, max_length=150)
    unresolved_mentions: list[str] = Field(default_factory=list, max_length=30)


class Evidence(Strict):
    id: str
    claim_id: str
    source_id: str
    revision_id: str
    chunk_id: str
    quote: str
    start: int
    end: int
    source_title: str
    source_kind: str
    source_updated_at: str
    indexed_at: str
    extraction_method: str
    ingestion_mode: str
    is_stale: bool
    is_current: bool


class Claim(Strict):
    id: str
    subject_id: str
    predicate: str
    object_id: str | None = None
    scalar: str | None = None
    scope: str
    evidence: Evidence


class Block(Strict):
    kind: Literal["fact", "inference", "uncertainty"]
    text: str
    evidence_ids: list[str] = Field(default_factory=list)


class Finding(Strict):
    id: str
    category: str
    title: str
    entity_ids: list[str]
    evidence_ids: list[str]
    path_id: str | None = None


class Edge(Strict):
    id: str
    source_entity_id: str
    target_entity_id: str
    predicate: str
    claim_ids: list[str]
    evidence_ids: list[str]
    conflict: bool = False


class PathDTO(Strict):
    id: str
    edge_ids: list[str]


class GraphDTO(Strict):
    nodes: list[Entity] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    paths: list[PathDTO] = Field(default_factory=list)


class Scope(Strict):
    visible_sources_considered: int = 0
    truncated: bool = False
    warnings: list[str] = Field(default_factory=list)


class Change(Strict):
    finding_id: str
    text: str
    evidence_ids: list[str] = Field(default_factory=list)


class Changes(Strict):
    added: list[Change] = Field(default_factory=list)
    removed: list[Change] = Field(default_factory=list)
    changed: list[Change] = Field(default_factory=list)


class Metrics(Strict):
    duration_ms: int = 0
    graph_query_count: int = 0
    graph_duration_ms: float = 0
    model_calls: int = 0
    model_id: str | None = None
    prompt_version: str = "1.2"
    agent_tool_calls: int = 0
    agent_rounds: int = 0


class AgentToolStep(Strict):
    tool: Literal[
        "resolve_entity",
        "search_evidence",
        "get_project_context",
        "trace_dependencies",
        "find_blockers",
        "find_ownership",
    ]
    round: int
    claim_count: int
    duration_ms: int


class Answer(Strict):
    run_id: str
    status: Literal["complete"] = "complete"
    answer_state: Literal[
        "supported", "partial", "conflict", "insufficient_evidence", "clarification", "needs_refresh"
    ]
    execution_mode: Literal["deterministic", "live_model"] = "deterministic"
    intent: str
    entity_id: str | None = None
    graph_epoch: int
    generated_at: str
    scenario_time: str
    blocks: list[Block] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    conflicts: list[Finding] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    graph: GraphDTO = Field(default_factory=GraphDTO)
    scope: Scope = Field(default_factory=Scope)
    changes: Changes = Field(default_factory=Changes)
    candidates: list[Entity] = Field(default_factory=list)
    metrics: Metrics = Field(default_factory=Metrics)
    historical: bool = False
    agent_trace: list[AgentToolStep] = Field(default_factory=list)


class InvestigateRequest(Strict):
    session_id: str
    question: str = Field(min_length=1, max_length=2000)
    entity_id: str | None = None
    previous_run_id: str | None = None


class PersonaRequest(Strict):
    persona: Literal["Engineer", "Lead", "Viewer"]


class Me(Strict):
    id: str
    persona: str
    groups: list[str]
    capabilities: list[str]
    demo: bool = True


class ProposalRequest(Strict):
    run_id: str
    entity_id: str
    assignee_id: str
    reason: str = Field(min_length=1, max_length=500)


class ConfirmRequest(Strict):
    proposal_id: str
    idempotency_key: str = Field(min_length=8, max_length=100)


class AccessRequest(Strict):
    expected_revision_id: str
    acl_groups: list[Literal["all_employees", "engineering", "leadership"]] = Field(max_length=3)


class RevisionRequest(Strict):
    fixture_id: Literal["t101_done", "t101_invalid", "restrict_runbook"]


class TicketStatusRequest(Strict):
    expected_revision_id: str
    status: Literal["open", "in_progress", "blocked", "done", "cancelled"]


class TicketDetails(Strict):
    source_id: str
    entity_id: str
    title: str
    expected_revision_id: str
    status: str | None
    blocked_entities: list[str]


class JobReceipt(Strict):
    job_ids: list[str]


class Plan(Strict):
    intent: Literal["release_risk", "change_impact", "owner_lookup", "decision_lookup", "evidence_search"]
    entity_id: str | None = None


class SourceMetadata(Strict):
    id: str
    kind: str
    title: str
    active_revision_id: str
    revision_number: int
    source_updated_at: str
    indexed_at: str
    acl_groups: list[str]
    ingestion_mode: str
    is_stale: bool
    state: str


class SourceList(Strict):
    items: list[SourceMetadata]
    total: int
    graph_epoch: int


class RevisionMetadata(Strict):
    id: str
    revision_number: int
    title: str
    source_updated_at: str
    indexed_at: str
    is_current: bool
    ingestion_mode: str


class JobStatus(Strict):
    id: str
    status: str
    stage: str
    source_id: str
    created_at: str
    fixture: bool = False
    revision_id: str | None = None
    unchanged: bool = False
    accepted: int = 0
    pending: int = 0
    unresolved_mentions: list[str] = Field(default_factory=list)
    graph_epoch: int | None = None
    error: str | None = None
    code: int | None = None


class ReviewDTO(Strict):
    id: str
    title: str
    reason: str
    assignee_id: str
    assignee_name: str
    entity_id: str
    evidence_ids: list[str]
    state: str
    graph_epoch: int | None = None
    expires_at_ms: int | None = None
    destination: str | None = None
    proposal_id: str | None = None
    created_by: str | None = None
    created_at: str | None = None
    idempotency_key: str | None = None


class ConversationDTO(Strict):
    id: str
    last_entity_id: str | None
    created_at: str


class HistoryDTO(Strict):
    id: str
    question: str
    status: str
    created_at: str
    session_id: str
    entity_id: str | None = None
