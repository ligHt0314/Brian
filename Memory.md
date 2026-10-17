# Company Brain — Project Memory and Handoff

Last updated: 17 October 2026 (IST). Owner: project team.

## Current reality

The active application is Company Brain for **BrightMart**, a completely fictional online grocery business. The user explicitly requested replacement of the previous small Orbit Labs seed with a medium-sized, easy-to-demonstrate dataset. `fixtures/brightmart` supersedes the original dataset assumptions in the seven planning documents. The stack remains Next.js, FastAPI, FalkorDB and operational SQLite, with one API process per graph.

The seed contains **200 sources, 180 entities and 432 accepted evidence-backed claims**: 40 people, 8 teams, 10 projects, 16 services, 10 customers, 60 tickets, 24 decisions and 12 registered commitment entities. Some entities deliberately have missing facts. Source kinds: 94 documents, 21 chats, 60 tickets, 24 decisions and one directory. Initial access: Engineer 196 records, Lead 200, Viewer 23.

Current graph: `company_brain_brightmart_demo`. The old graph was reversibly renamed `retired_company_brain_orbit_demo_20261017`. Old operational records were preserved in SQLite table `retired_orbit_records_20261017`; active history started empty. Old original uploads were preserved. Automatic approval review rejected permanent graph/upload/history deletion because dataset replacement did not clearly authorize erasing operational history; the reversible archive was used instead. Old fixture files were removed from application source. No non-demo graph was reset or deleted.

## The demo story

BrightMart helps local grocery stores sell online. Easy Checkout uses Checkout Service, which depends on Payment Gateway. T-101 blocks Payment Gateway. C-101 promises the checkout rollout to Green Basket Stores by 18 October. The Payments runbook and Integrations handoff disagree about the current owner. Maya Rao and Dev Shah have documented contributions, separately from ownership.

Other projects: Sales Dashboard, Delivery Tracking, Quick Refunds, Stock Alerts, Store Pickup, Customer Rewards, Seller Dashboard, Help Center and Fresh Subscriptions. Payment Gateway also has dependencies from refunds and subscriptions, making impact analysis useful across projects. The dataset intentionally includes inactive tickets, unknown status, stale sources, ambiguous aliases, missing ownership and leadership-only records.

Scenario clock: **17 October 2026, 10:00 AM IST**, fixed for reproducibility. Actual ingestion/run timestamps use real time. Updating T-101 to done removes its active blocker status; it does not establish launch readiness or resolve the ownership conflict.

## Workspace guide and dataset reference

- App: http://localhost:3000/investigate
- Workspace handbook: http://localhost:3000/guide
- Presenter script: docs/BrightMart-Demo.md
- Full readable source book: docs/BrightMart-Sourcebook.md
- Reproducible generator: scripts/build_fixtures.py; no network/model calls required.
- Manifest and registry: fixtures/brightmart.

The guide introduces the business, explains how graph reasoning works, offers editable example questions for all ten projects, defines all sixteen systems, and walks through evidence, ownership review, status updates and permission changes. Its metadata describes the published synthetic seed, not current private-source counts. The source book includes all synthetic access levels and is a local artifact, not a public source-access endpoint.

## Implemented behavior and limits

Permission-scoped graph investigations; exact-span source citations; dependencies and conditional impact; ownership conflicts and contributors; recorded decisions; immutable revision activation; text/structured imports; source history; private conversations/history; changed-answer explanations; confirmed internal review tasks. FalkorDB is canonical for company facts and reviews. SQLite holds operations and derived artifacts. Shared source-policy/mutation locking and epoch checks remain mandatory; model calls stay outside the lock.

Gemini uses the private server key and user-approved `gemini-3.1-flash-lite`. The agent selects reviewed read tools, observes actual results and may select more reads. Six reads total, two selection rounds and three dependency hops remain. The medium seed required increasing the permission-filtered repository snapshot from 150 to **2,000 claims**, and answer excerpts from 16 to **32**; each selected tool still returns at most 150 claims, model observations remain limited to 16 passages, and graph display remains 30 nodes/50 edges. Graph projection now removes edges/paths when their nodes are outside the display budget. Truncation stays visible. Conditional-impact answers prioritize dependency/promise evidence rather than unrelated active work items.

The Sources UI consumes all permitted pagination pages and checks epoch consistency. Public entity lookup returns up to 200 entries (capped at 250), so new projects and people are discoverable. OpenAPI and frontend types were regenerated.

## Verification observed this session

- 41 backend tests passed, including real isolated FalkorDB graphs and new full-corpus exact-span, count, pagination, access and cross-project cases.
- 24/24 deterministic evaluation cases passed on BrightMart seed 2.0; 30 warm engine runs median 54 ms / p95 63 ms, excluding HTTP, browser and model latency.
- Live Gemini gate passed on an isolated graph: unseen Markdown extracted two exact-quote claims, new evidence was retrieved, release investigation used five reads over two selection rounds, and Viewer isolation passed. Observed release run 16.2 seconds. See artifacts/gemini-live-verification.json. Broad human semantic quality and token cost remain unscored.
- Ruff, OpenAPI synchronization and strict TypeScript checks passed. Production Next.js build passed.
- Docker registry metadata resolution stalled. Application runtimes already cached on this computer were used to package the changed API sources and locally built standalone web output. Standard Dockerfiles remain the reproducible fresh-build path. `make up BUILD_FLAG=--no-build` started the complete updated stack from those images; default `make up` still builds normally.
- All 10 desktop/mobile Playwright cases passed, including the new guide, editable example questions, all-project discovery and searching the second source page. Browser source updates restored T-101 to blocked afterward.

## Operating instructions

Use `make up`; when the application images have already been built and the registry is unavailable, use `make up BUILD_FLAG=--no-build`. Keep one API process. Keep `.env` private; it contains the existing Gemini key and signing/operator secrets. Never print it or run `docker compose config` into shared logs.

All backend tests and live-provider gates create isolated random graphs. Do not reset the working demo for incidental cleanup. Browser demonstration tests intentionally change the synthetic demo and restore T-101's blocked state. The operator-only reset endpoint accepts exactly the configured BrightMart synthetic graph and requires the private token. It retains private history and revalidates it on read.

The one-time `scripts/replace_demo_dataset.py --replace-orbit` migration requires the API to be stopped; it validates the new corpus before reversibly retiring the exact old graph and records table. It preserves original uploads. It is not a general graph deletion utility.

## Remaining release gates

Human factual-support review, broad model-quality evaluation, production identity, arbitrary-company onboarding, live external connectors, multitenancy, public deployment and competition submission remain incomplete. There are no external messages, Jira writes, autonomous launch approvals or enterprise security claims. Seed extraction is reviewed fixture data; live extraction is demonstrated separately and must remain labeled.

Historical context: the original Orbit prototype was verified on 15 October with 35 backend tests, a 24-case deterministic corpus, desktop/mobile browser cases and controlled persistence checks. Those results applied to that small seed. Current dataset counts and observed checks above supersede its handoff advice. The original seven planning documents remain the behavioral baseline except for the explicitly authorized dataset/budget extension recorded here and in Architecture.md.


## Product MVP presentation and ticket operations — 17 October 2026

The user requested a professional workspace presentation and removal of demo/synthetic wording from the website. App navigation, headers, profile labels, onboarding and footer now use workspace language. The data's provenance remains documented here and in fixtures/source records; no production-authentication claim was added. Role sessions remain local role previews.

The guide is now WorkspaceGuide, with access-filtered live source counts, a project directory, searchable people directory, system glossary and practical question workflows. The homepage has working source/project/people/review navigation metrics, consistent typography and responsive styling. Internal import labels are shown as Reviewed import / Reviewed extraction or Model extraction, preserving truthful provenance. Model fallback labels remain visible.

Sources now offers a general ticket-status editor rather than the T-101 fixture shortcut. GET /sources/{id}/ticket and POST /sources/{id}/ticket-status validate Lead/import access and current source ACL; stale revision edits fail with 409. Edits preserve all other claim quotes, contributors, pending scores and validity intervals, activate a new immutable revision, and use reviewed human-record provenance without an LLM call. Overlapping evidence that cannot safely be rewritten requires source-file editing. Changes feed ordinary investigation reruns and the existing change summary. API contracts/types were regenerated.

41 backend tests passed, including three new status-edit cases. Ruff, strict TypeScript, OpenAPI synchronization and production web build passed. The 24-case deterministic regression passed. Its timing sample now also uses an isolated graph: an inherited obsolete FALKORDB_GRAPH environment variable exposed that the old timing sample depended on the working graph. No active graph was reset to fix it.

Read docs/Product-MVP.md for the functional scope and remaining deployment/identity gates. The website's new labels do not make role preview into production sign-in. No real company data or external write was introduced. Existing records, histories, reviews, source ACLs and the archived retired dataset were preserved.

Final product-interface browser gate: all 10 desktop/mobile cases passed in 1.1 minutes, including the general status editor, revision-driven changed answers, handbook wording checks and people search. Current product screenshots use the artifacts/workspace- prefix. The production web build and final make check passed.


## Repository setup documentation — 17 October 2026

The user initialized an empty Git repository and requested a run-focused README, appropriate ignore rules and advice about publishing the dataset. README.md now documents prerequisites, private configuration generation, Gemini setup, Docker/Make commands, automatic fixture loading, everyday operation, troubleshooting, alternate ports, host development and checks. fixtures/brightmart/README.md explains fictional provenance, contents, checksums and reproducible generation.

.gitignore now covers environment variants while permitting .env.example; private uploads, state and database dumps; dependency/build/test caches; logs, local editor/agent state; artifacts/ bundles/media and generated evals/results/. The empty root package-lock.json is ignored because the Node application and required lockfile live in apps/web. Source fixtures, the generator, golden questions, API contracts and all required application lockfiles remain eligible for Git.

Observed verification: 15 required source/template/config paths remain unignored; 16 representative secret/runtime/generated paths are ignored; all 200 fixture checksums match the manifest; the first-run configuration script generates private secrets and preserves an existing configuration in an isolated temporary checkout. A local content check found none of the configured private credentials or recognizable API/PAT/private-key formats in Git candidate text files. No secret contents were printed, no source facts or running data were changed, and no files were staged, committed or pushed. The repository index remained empty.
