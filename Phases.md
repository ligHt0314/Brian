# Company Brain — Delivery Phases

Version: 1.0 · Planning date: 15 October 2026 · Planning baseline; actual phase/gate status is recorded in Memory.md.

## 1. Planning assumptions

The baseline assumes a small team with roughly 28–36 focused elapsed build hours across four calendar days. Estimates are planning ranges, not promises. [ImplementationPlan.md](ImplementationPlan.md) provides executable task breakdowns. Use [Memory.md](Memory.md) to record actual progress and revised estimates.

The published deadline is 18 October 2026, 11:59 PM IST. Aim to submit by 9:00 PM IST to leave recovery time. Verify the submission form and required materials directly before the final day. [Event page](https://www.wemakedevs.org/hackathons/falkordb)

## 2. Phase 0 — Lock the contract and prove connectivity

Target: 15 October · 1–2 hours · Tasks IP-01–IP-02.

Read all seven documents. Establish the repository, environment template, dependency locks, Docker services, typed schemas, health checks, and a single verified FalkorDB read/write operation. Confirm the selected LLM can return structured output through the provider adapter. Declare the chosen versions and model in Memory.

Exit gate: a fresh checkout starts the services; API readiness reflects graph connectivity; empty UI loads; a graph record survives a controlled database restart after the configured persistence flush. No product UI can claim connected sources yet.

Failure response: fix infrastructure before expanding scope. Use the team's known deployment host or local Docker if hosted provisioning consumes the timebox.

## 3. Phase 1 — Create trustworthy company evidence

Target: 15 October · 5–7 hours · Tasks IP-03–IP-05.

Implement the entity registry, Claim/Source/Revision/Chunk model, eligible-source filtering, structured ingestion, source revision activation, and the canonical synthetic dataset. Add readable source inspection endpoints. Build the Sources screen against real ingestion state.

Exit gate: 24 source records load; every active claim resolves to a real span; reimport is idempotent; two ownership assertions remain separate; restricted content is excluded before retrieval; failed revision staging does not replace the previous active revision.

Evidence checkpoint: inspect the canonical blocker path directly in FalkorDB, including each intermediate Claim and its source chunk.

## 4. Phase 2 — Deliver a working investigation

Target: 16 October · 6–8 hours · Tasks IP-06–IP-08.

Implement the query templates, blocker/commitment reasoning, ownership conflict detector, agent plan validation, answer schema, and evidence mapping. Add typed API integration and the investigation page. Show the evidence drawer and focused graph path.

Exit gate: ask the canonical release question through the UI and receive a real graph-derived answer; a paraphrase works; an unsupported question is honest; an ambiguous entity asks for clarification; every graph edge opens evidence.

Scope checkpoint: if this does not work by the end of 16 October, stop visual polish and all optional integrations. Keep structured inputs working while model extraction is completed in Phase 3.

## 5. Phase 3 — Demonstrate memory and useful action

Target: 17 October · 6–8 hours · Tasks IP-09–IP-11.

Implement text extraction with exact evidence spans, durable session context, fresh retrieval for follow-ups, answer change comparison, and internal review-task confirmation. Integrate source history and the mutation controls used in the demo.

Exit gate: import a previously unseen small Markdown document using live extraction; update T-42; rerun and show the removed blocker; reload the browser and continue the same project context; create one review task exactly once despite repeated confirmation; revoke a source and verify old answers do not leak its content.

Demo checkpoint: record a rough uninterrupted walkthrough now. Its failures become the final day's work list.

## 6. Phase 4 — Validate, polish, and package

Target: 18 October · 6–8 hours · Tasks IP-12–IP-14.

Complete the 24-question evaluation, graph integration checks, permission cases, browser journey, deployment checks, accessibility fixes, and setup documentation. Record actual latency/cost results and limitations. Finish the video and submission narrative.

Exit gate: all P0 release checks in ImplementationPlan pass; the deployment or local package starts from documented steps; a fallback video exists; no secret appears in the repository or recording; the submission form has accepted all required materials.

Suggested final-day schedule in IST: feature freeze by noon; validation and fixes through 4:00 PM; recording and setup rehearsal through 7:00 PM; submission by 9:00 PM. If the event is already further along when implementation begins, compress scope rather than assuming these dates are still available.

## 7. Staffing options

| Team size | Suggested organization |
|---|---|
| One | Build the vertical slice sequentially; use fixture imports, basic CSS, and evidence path lists before graph polish |
| Two | One owns data/API; one owns UI/fixtures/docs; agree schemas before simultaneous implementation |
| Three | Data/ingestion; agent/API; UI/demo. Rotate one reviewer onto integration checks |
| Four | Data/ingestion; agent/retrieval; frontend/design; evaluation/deployment/demo |

These are suggested human workstreams, not an instruction to spawn agents automatically. The same task IDs apply to every team size.

## 8. Scope-cut order

Remove in this order if behind: live connectors; vector search; conflict resolution editing; whole-company graph browsing; animations; nonessential visualizations; optional comparison benchmarks. All are P1/P2 or presentation extras.

Preserve source citations, graph-based relationship reasoning, permission filtering, one source update, contradiction display, internal review-task creation, and clear failure behavior. For a solo team, simplify UI chrome and retain the same evidence contract. If a P0 cannot be completed, disclose it in the submission and Memory rather than relabeling it as complete.

## 9. Stop/go gates

| Checkpoint | Stop condition | Next action |
|---|---|---|
| End Phase 0 | Graph connection or persistence unreliable | Repair infrastructure; defer deployment |
| End Phase 1 | Evidence cannot be traced or access leaks | Fix data model/filtering before agent work |
| End Phase 2 | Answer relies on hardcoded question behavior | Replace with generic graph tools and typed facts |
| End Phase 3 | Update changes wording but not retrieved evidence | Inspect revision activation and epoch invalidation |
| Release | Any restricted data leakage | Block release until fixed; never waive this gate |
| Release | Latency target missed but correct behavior works | Report measured latency; reduce graph/model budgets |

## 10. Milestone reporting template

For each milestone, record: date/time; phase and task IDs; completed behavior; validation evidence; known failures; updated estimate; next task. Use concise factual statements. A phase becomes COMPLETE only after its exit gate is demonstrated.
