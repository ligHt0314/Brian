# Company Brain contributor instructions

Read `Rules.md` and `Memory.md` before changing the application. The seven planning documents remain the requirements baseline; Memory and the verification report distinguish implemented behavior from unverified gates.

- Start the complete local package with `make up`. Use only one API process against a graph.
- FalkorDB is canonical for company facts and reviews. SQLite stores operational records and derived run artifacts.
- Preserve per-source evidence, revision lifecycle, source ACL checks and the shared mutation/access snapshot lock. Keep model calls outside that lock.
- Tests must use isolated random graph names. Never reset the working demo as incidental test cleanup.
- Run relevant checks; regenerate API types with `make contract` after contract changes.
- Keep model keys and local secrets in ignored `.env`. Do not claim live extraction, human-rated support or deployment without observed verification.
