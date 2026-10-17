# Company Brain — Product Requirements

Version: 1.0 · Prepared: 15 October 2026 · Status: requirements baseline; local implementation and observed gates are recorded in Memory.md.

## 1. Product decision

Build **Company Brain**, a launch-readiness and change-impact assistant for a small software company. It connects company records in FalkorDB and helps a product or engineering lead answer: **“What could block this launch, who can help, and what evidence supports that conclusion?”**

The first product is deliberately focused on release decisions. A user can investigate a project, inspect its dependencies and customer commitments, see competing ownership claims, and create an internal review task. After a source changes, the next investigation must use the new state and explain which findings changed.

Success means a stranger can complete the main workflow and understand why a graph was useful. Winning a hackathon cannot be guaranteed; the design prioritizes a useful problem, a visible graph contribution, working behavior, clear evidence, and a memorable demonstration.

## 2. Document map and authority

Read in this order: this file → [Architecture.md](Architecture.md) → [Rules.md](Rules.md) → [Design.md](Design.md) → [Phases.md](Phases.md) → [ImplementationPlan.md](ImplementationPlan.md) → [Memory.md](Memory.md).

| Document | Owns |
|---|---|
| PRD.md | User problem, product scope, requirement IDs, acceptance outcomes |
| Architecture.md | Data schema, service boundaries, API contracts, algorithms |
| Rules.md | Implementation invariants and contribution requirements |
| Design.md | Screens, components, interaction behavior, accessibility |
| Phases.md | Delivery order, time allocation, scope cuts, milestone gates |
| ImplementationPlan.md | Build tasks, file ownership, dependencies, validation |
| Memory.md | Decisions, current status, handoff protocol, unresolved choices |

Architecture owns technical field names. PRD owns scope. If a proposed change affects both, update both in the same change. Memory records reality and never silently overrides these contracts.

## 3. Audience and problem

Primary user: a product or engineering lead at a software team with 20–150 people. They need to prepare a release review across project documents, team conversations, issue records, and customer promises.

Secondary user: an engineer joining a project or investigating a dependency. They need the current owner, relevant prior work, and the rationale behind a decision.

The working hypotheses are that evidence is scattered, decisions outlive their context, and changes do not reach everyone affected. These are hypotheses for this product, not claims that every competing platform lacks the relevant capability. Validate them with three short user conversations if people are available: ask for a recent release surprise, the tools involved, and the time spent reconstructing what happened.

### Competitive context

Glean already connects content and people through a knowledge graph; Guru already addresses verification; Notion and Rovo already provide connected search. A graph, citations, or a chat box alone are insufficient differentiation. The proposed distinction is an unusually complete release investigation: evidence paths, explicit uncertainty, source revision changes, and a review action in one workflow.

References: [Glean Search](https://docs.glean.com/administration/search/about), [Guru verification](https://help.getguru.com/docs/what-is-verifcation), [Notion Enterprise Search](https://www.notion.com/en/help/enterprise-search), [Atlassian Rovo](https://www.atlassian.com/platform/artificial-intelligence).

## 4. Hackathon fit

The event runs 15–18 October 2026, with submissions closing at 11:59 PM IST on 18 October. The Company Brain track emphasizes connected company knowledge, ownership, decision sources, freshness, and sourced answers. FalkorDB must be the primary graph database and central to the product. The main submission implementation must be new during the event; a live deployment is preferred, with a working video and complete local setup as the alternative. These are event requirements, not a published scoring formula. [Official event page](https://www.wemakedevs.org/hackathons/falkordb)

## 5. Core journeys

### Journey A: investigate a release

1. Lead opens the seeded Orbit Labs workspace and selects Atlas SSO.
2. Asks “What could block Atlas SSO, and which customer commitment is affected?”
3. Agent resolves the project, follows dependencies, retrieves open blockers and commitments, and identifies ownership evidence.
4. Answer contains risk cards, a scope statement, source citations, and a compact relationship path.
5. User clicks an edge or citation to inspect its original evidence.

### Journey B: handle conflicting ownership

1. User asks who owns Directory Sync.
2. A runbook identifies Platform; a chat claims Integrations took over.
3. Product displays competing claims with dates and evidence, without selecting a winner solely by recency.
4. It separately shows relevant contributors as possible people to consult.
5. User previews and confirms an internal review task assigned to a named directory person.

### Journey C: observe a change

1. An operator imports a revised record for ticket T-42 through the normal ingestion pipeline.
2. Sources UI displays the new indexed revision and completion time.
3. User reruns the launch investigation.
4. T-42 no longer appears as an active blocker; the prior result remains an explicitly historical answer.
5. UI explains the removed risk and cites the revision that changed it. Ownership uncertainty can remain independently unresolved.

## 6. Requirements and acceptance criteria

P0 is required for the submission. P1 is useful only after every P0 gate passes. P2 is outside this event's committed scope.

| ID | Priority | Requirement | Acceptance |
|---|---|---|---|
| FR-01 | P0 | Import JSON source envelopes and UTF-8 Markdown/plain text | Upload creates a tracked job; valid evidence reaches FalkorDB; malformed input returns actionable errors |
| FR-02 | P0 | Ingest docs, chat exports, tickets, decisions, directory records | All five types exist in the fixture corpus; source type is visible |
| FR-03 | P0 | Resolve entities and their aliases | Stable IDs join records; ambiguous aliases prompt a choice; no silent entity merge |
| FR-04 | P0 | Answer release, impact, owner, and decision questions | Supported intents execute graph tools and return the typed answer contract |
| FR-05 | P0 | Trace answers to evidence | Every substantive factual statement has valid evidence IDs; every rendered graph edge has supporting claims |
| FR-06 | P0 | Follow multiple relationships | A blocker path crosses project → service → dependency → ticket and links affected commitments |
| FR-07 | P0 | Represent conflicting claims | Both eligible ownership assertions appear; answer explicitly marks conflict |
| FR-08 | P0 | Update knowledge without losing provenance | Revision activation changes current answers; old revisions remain available in authorized source history |
| FR-09 | P0 | Enforce source permissions | Hidden source content, titles, counts, paths, and citations do not reach an unauthorized response or model request |
| FR-10 | P0 | Create an internal review task | Preview then explicit confirmation; task survives restart; repeat confirmation is idempotent |
| FR-11 | P0 | Handle missing evidence honestly | Unsupported, ambiguous, partial, and unavailable cases have distinct states |
| FR-12 | P0 | Persist investigations and follow-up context | Session stores IDs and run summaries; follow-up resolves its project then retrieves fresh evidence |
| FR-13 | P0 | Provide operational visibility | Source freshness, ingestion failures, execution mode, query counts, and actual timings are inspectable |
| FR-14 | P1 | Semantic retrieval | Add embeddings only if keyword/entity retrieval misses a measured class of questions |
| FR-15 | P1 | Review resolution workflow | Authorized person can resolve a conflict through a new auditable source record |
| FR-16 | P1 | One live connector | Implement one import/sync connector with its actual permissions and cursor behavior |
| FR-17 | P2 | Broad enterprise rollout | SSO, production tenant provisioning, arbitrary connectors, mobile app, billing, and external autonomous actions |

## 7. Exact MVP boundaries

One synthetic organization, three server-defined demo identities, a small trusted directory, one running API process, a persistent graph, a persistent job/session store, and a browser UI. Seeded export files are labeled as exports; they do not imply a live Slack/Jira connection. At least one newly supplied document must be processed through model extraction during the demonstration or recorded walkthrough.

Core execution uses one orchestrating agent with constrained tools. It can select a supported investigation and call tools in bounded steps. It cannot execute arbitrary Cypher, arbitrary URLs, or shell commands. Questions outside supported intents fall back to evidence search or an honest scope explanation.

The internal ReviewTask is the P0 action. Sending emails, posting to Slack, changing external tickets, and automatically declaring a launch approved are outside P0. A completed blocker is not evidence that the entire project is ready.

## 8. Canonical demo world

Organization: fictional **Orbit Labs**. Main project: **Atlas SSO**. Customer: **Meridian Retail**. Main services: **Auth Gateway** and **Directory Sync**. Engineers: **Maya Rao** and **Dev Shah**. Teams: **Platform** and **Integrations**.

Required evidence chain:

- Atlas SSO `USES` Auth Gateway.
- Auth Gateway `DEPENDS_ON` Directory Sync.
- Ticket T-42 `BLOCKS` Directory Sync and has `STATUS=blocked`.
- Commitment C-7 `REQUIRES` Atlas SSO, is `MADE_TO` Meridian Retail, and is due on 18 October 2026.
- Decision D-9 is `ABOUT` Atlas SSO; its cited text requires enterprise SSO and rules out password fallback for the promised rollout.
- Directory Sync has separate `OWNED_BY` assertions naming Platform and Integrations. Their scopes and validity overlap.
- Maya and Dev have independently evidenced `WORKED_ON` links; expertise does not establish ownership.

Initial dataset: exactly 24 source records: 1 directory, 6 documents, 5 chat threads, 8 ticket records, and 4 decision records. Aim for 80–150 supported claims, not an artificial claim quota. Include an unrelated project, duplicate aliases, an old runbook, and a leadership-only note. Three revision fixtures exercise T-42 completion, a failed update, and an ACL restriction. Use a fixed scenario clock, 15 October 2026 at 10:00 AM IST, for reproducible demo calculations; show that it is a simulation clock.

## 9. Product outcomes and release gates

These are targets to measure, not achieved results:

| Outcome | Target / gate |
|---|---|
| Grounded facts | 100% citation-ID validity; ≥90% human-rated factual support on the evaluation set |
| Release investigation | Correct required blocker and commitment paths on all canonical cases |
| Permission isolation | Zero restricted-data disclosures across all defined access cases |
| Change handling | Correct result after a source update; no mixed source revision within one answer |
| Ingestion | Reimport causes no duplicate claims; failed revision leaves prior current evidence usable |
| Interactive response | Warm p95 ≤15 seconds on declared demo hardware; report actual values |
| Source update | ≤10 seconds for a small structured revision; ≤30 seconds for a small model-extracted document |
| Honest uncertainty | All unanswerable and conflicting canonical cases use the appropriate state |
| Completion | Fresh setup, persistent restart, and a rehearsed end-to-end demo succeed |

Evaluate 24 questions: 4 direct facts, 6 relationship questions, 4 ownership/decision questions, 4 update cases, 3 access cases, and 3 ambiguity/unknown cases. Record expected evidence and paths before looking at model answers. Use the same accessible corpus and model for any retrieval comparison; do not claim universal GraphRAG superiority from this small dataset.

## 10. Demo script and submission package

Target a 3–4 minute product demonstration: establish a launch question; reveal the blocker path and affected commitment; inspect a source; expose the ownership conflict; confirm a review task; ingest T-42 revision; rerun and show the changed conclusion. If time permits, switch to a different demo identity and show permission-scoped results.

Submission package: application or reproducible local run, repository README, architecture diagram, synthetic data disclosure, demo video, measured evaluation summary, limitations, and clear instructions for supplying an LLM key. Optional blog post explains the problem, graph modeling, update behavior, and observed evaluation results. Never present seeded facts as actual company data or a canned response as a live model result.

## 11. Risks and scope decisions

Entity extraction and evidence quality are the largest technical risks; build structured ingestion and the evidence model first. Connector authentication and broad search can consume the whole event; keep exports as P0. Graph visualizations can become unreadable; show only the answer's relevant subgraph. Keep production enterprise readiness claims out of the pitch. If time shrinks, preserve evidence, updates, and access boundaries and cut optional retrieval modes and connector work.
