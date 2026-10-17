# Company Brain

Company Brain connects projects, people, tickets, decisions and customer commitments so you can investigate risks, trace dependencies and act on source-backed findings. The application runs locally with **Next.js**, **FastAPI**, **FalkorDB** and an optional **Gemini** API connection.

The repository includes **BrightMart**, a reproducible fictional online-retail company with 200 sources, 180 entities and 432 supported claims. You can start exploring immediately without connecting company accounts or importing your own data.

## Requirements

For the complete application:

- Docker Desktop, or Docker Engine with Docker Compose v2. Start Docker before continuing.
- Python 3, used to generate local configuration.
- `make` if using the Makefile commands. Equivalent Docker commands are provided below.
- Internet access for the first image build and for live Gemini requests.

You do **not** need to install Node.js, Python application dependencies or FalkorDB on your computer for the Docker setup.

## Quick start

Run these commands from the repository root, where `compose.yaml` lives.

### 1. Create your local configuration

```sh
python3 scripts/init_env.py
```

This creates an ignored `.env` with generated session and operator secrets. It preserves an existing `.env`. Use this script rather than copying the placeholder secrets from `.env.example`.

### 2. Configure Gemini

Open `.env` in your editor and set:

```dotenv
LLM_PROVIDER=openai-compatible
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
LLM_MODEL=gemini-3.1-flash-lite
LLM_API_KEY=your-gemini-api-key
```

Keep the generated secrets and other defaults. The key stays on the backend; do not add it to frontend code or any `NEXT_PUBLIC_` variable.

A model key enables live question planning, agent tool selection, answer synthesis and Markdown/text extraction. Without one, the included dataset still supports clearly labeled deterministic graph investigations and structured ticket updates.

### 3. Start the application

```sh
make up
```

Without `make`:

```sh
docker compose up --build -d
```

The first build downloads dependencies and can take several minutes. Startup automatically loads missing BrightMart records; it preserves existing source revisions and does not require a separate seed command.

Open:

- **[Workspace](http://localhost:3000/investigate)** — run investigations.
- **[Workspace guide](http://localhost:3000/guide)** — browse projects, people and terminology.

Only port **3000** is exposed, on your computer's loopback interface. The API and database stay inside the Docker network. Another computer's `localhost` does not point to this installation.

## Try the main workflow

1. With the **Engineer** workspace role selected, click **Find launch risks** or ask:

   > What could block Easy Checkout, and which customer commitment is affected?

2. Open a numbered citation to inspect the exact source passage. Use the Graph tab to follow the project → system → payment dependency and its blocking ticket.
3. Ask who owns Payment Gateway. Compare the conflicting ownership records and contributors, then preview and confirm an internal review task.
4. Switch to **Lead**. In **Sources → Update ticket status**, select **T-101**, choose **Done**, and save.
5. Reopen the Lead investigation in **History** and rerun it. “What changed” explains the removed blocker using the revised status evidence.
6. You can use the same status editor to return T-101 to **Blocked**. Switch to **Viewer** to see how source access limits the findings.

Roles are local access previews: **Engineer** investigates and creates reviews, **Lead** can also import and update sources, and **Viewer** has limited source access. They are not production user authentication.

## Everyday commands

| Task | Command |
| --- | --- |
| Build and start the complete stack | `make up` |
| Start existing images without rebuilding | `make up BUILD_FLAG=--no-build` |
| Stop the stack and retain its data | `make down` |
| Resume stopped containers | `docker compose up -d` |
| Check container status | `docker compose ps` |
| Follow application logs | `docker compose logs -f api web` |
| Reload `.env` changes in the API | `docker compose up -d --force-recreate api` |
| Rebuild after changing application code | `make up` |

FalkorDB uses the `graph-data` Docker volume. Private uploads, sessions, jobs and investigation artifacts use `api-data`. Both survive ordinary restarts and `docker compose down`. **`docker compose down -v` deletes these volumes**; it is not a normal stop command.

Do not share `.env`, publish database dumps, or paste the output of `docker compose config`, which can contain resolved credentials.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| Cannot connect to the Docker daemon | Start Docker Desktop or the Docker service, then run `make up` again. |
| The image registry is unavailable | If the application images were built previously, use `make up BUILD_FLAG=--no-build`. A fresh build needs registry access. |
| Port 3000 is already in use | Stop the conflicting application, or follow the alternate-port command below. |
| Gemini requests fail | Check the key, provider URL, model access and quota; recreate the API container after editing `.env`. Investigations expose their graph-only fallback. New text extraction requires a working provider. |
| The answer still reflects older source data | Rerun the investigation after the import or ticket update completes. |
| Host development uses an unexpected graph | Remove old exported `FALKORDB_*`, `SQLITE_PATH` or `UPLOAD_DIR` values from that terminal. Process environment variables take precedence over `.env`. |

To use another local port, change both the published port and the allowed browser origin:

```sh
WEB_PORT=3001 ALLOWED_ORIGIN=http://localhost:3001 docker compose up --build -d
```

Then open `http://localhost:3001`. Use the same overrides when recreating those containers. On PowerShell, set the two environment variables with `$env:NAME="value"` before running Docker Compose.

## Host development

Use this setup when editing the API or web application outside Docker. In addition to Docker, install **Python 3.12+**, **uv**, **Node.js 22+** and **npm**. The Makefile expects a Unix-like shell; Windows developers can use WSL.

Stop the container API and web app first. **Run only one API process against a graph.**

```sh
docker compose stop api web
make setup
make dev
make seed
```

`make setup` installs the locked Python and frontend dependencies. On Linux/WSL, use `make setup UV_CACHE_DIR=/tmp/company-brain-uv` to override the Makefile’s macOS cache path. `make dev` starts FalkorDB with its development port on `127.0.0.1:6389`. `make seed` imports missing fixtures without overwriting existing revisions.

Start the API and frontend in separate terminals at the repository root:

```sh
# Terminal 1
make api
```

```sh
# Terminal 2
make web
```

The web app runs at `http://localhost:3000`; the host API runs at `http://127.0.0.1:8000`. Its interactive API reference is at `http://127.0.0.1:8000/docs`.

## Checks

These commands require the host-development dependencies installed by `make setup`:

```sh
make check        # Ruff, OpenAPI/type synchronization and strict TypeScript
make build        # Production frontend build
make test-unit    # Domain and provider unit tests
make test-graph   # Real FalkorDB integration tests
make evaluate     # 24 deterministic cases and an isolated warm timing sample
make test-e2e     # Desktop/mobile browser workflows; requires Google Chrome
```

Graph checks use isolated random graphs. To expose the development database port while keeping the complete container stack running:

```sh
docker compose -f compose.yaml -f compose.dev.yaml up -d
```

Browser tests use the running local workspace. They create internal review records, update T-101 and restore its blocked status afterward; run them against the included fictional data only.

Smoke-check the complete Docker stack:

```sh
BRAIN_API_URL=http://127.0.0.1:3000 make smoke
```

`make contract` regenerates the checked-in OpenAPI and TypeScript definitions after API contract changes. Ordinary backend/evaluation tests disable paid provider calls. The optional live extraction/agent check is separate and **uses your configured API key**:

```sh
PYTHONPATH=services/api .venv/bin/python scripts/verify_live_model.py
```

Observed local checks and their limits are documented in [docs/Verification.md](docs/Verification.md).

## Dataset and GitHub

**The BrightMart fixtures are intended to be committed with the project.** They are generated fictional records, not a real company's exports or a copy of the running database. The included names, customers, tickets and leadership-only markers are invented. Access labels exercise application filtering; they do not make these particular fictional fixtures private company information.

Commit the following with the application source:

- `fixtures/brightmart/` — source bodies, exact-span claims, registry and checksummed manifest.
- `scripts/build_fixtures.py` — the reproducible dataset generator.
- `evals/questions.jsonl` — regression questions kept separate from application facts.
- `.env.example`, `compose.yaml`, `compose.dev.yaml`, `Makefile` and the Dockerfiles.
- `apps/web/package-lock.json`, `uv.lock`, `requirements.lock` and the generated API contracts.

Regenerate the fixture files and workspace catalog with:

```sh
python3 scripts/build_fixtures.py
```

This rewrites the checked-in fixture files and reference material; **it does not reset an already running graph**. Startup only inserts missing sources. See [the dataset guide](docs/BrightMart-Demo.md) and [the readable source book](docs/BrightMart-Sourcebook.md) for the records and walkthrough.

Do **not** commit `.env` or its variants, `.data/`, private uploads, local database files/dumps, dependency folders, build output, browser traces, logs or generated source bundles. `.gitignore` covers those paths, including `artifacts/` and `evals/results/`. GitHub viewers receive the fixture files and can regenerate the workspace without receiving your key or current operational history. Review new imports separately before adding them to Git.

## Project layout

```text
apps/web/                 Next.js interface and generated API types
services/api/             FastAPI, agent tools, ingestion and graph reasoning
fixtures/brightmart/      Reproducible fictional company dataset
scripts/                  Setup, seed, contract, verification and packaging tools
infra/                    Dockerfiles and database configuration
tests/e2e/                Desktop and mobile browser workflows
evals/questions.jsonl     Deterministic regression inputs
docs/                     Product guide, architecture and verification notes
```

## Architecture and scope

The browser talks to FastAPI through the same-origin Next.js proxy. Gemini plans the question and chooses reviewed read tools; FalkorDB provides permission-filtered facts and relationship paths. Graph reasoning constructs the findings, with citations and explicit conflicts. Investigations are bounded to six reads, two selection rounds and three dependency hops. SQLite stores operational state and derived answers; company facts and confirmed reviews remain canonical in FalkorDB.

This is a functional local MVP for the included corpus. Production sign-in, multi-company onboarding, live Slack/Drive/Jira connections, public hosting and broad human-rated answer evaluation remain separate work. Internal review creation and ticket status edits do not send messages or modify external services. See [docs/Product-MVP.md](docs/Product-MVP.md), [Architecture.md](Architecture.md) and [Memory.md](Memory.md) for the implementation boundaries.
