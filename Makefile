SHELL := /bin/bash
PY := .venv/bin/python
export PYTHONPATH := services/api
export UV_CACHE_DIR := /private/tmp/company-brain-uv
BUILD_FLAG ?= --build
.PHONY: setup dev seed check contract test-unit test-graph test-e2e evaluate smoke demo-reset
setup: .env
	uv sync --frozen
	cd apps/web && npm ci
up: .env
	docker compose up $(BUILD_FLAG) -d
down:
	docker compose down
dev: .env
	docker compose -f compose.yaml -f compose.dev.yaml up -d falkordb
	@echo 'Run make api and make web in separate terminals.'
api:
	.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
web:
	cd apps/web && npm run dev
seed:
	$(PY) scripts/seed.py
contract:
	$(PY) scripts/export_openapi.py
	cd apps/web && npx openapi-typescript lib/api/openapi.json -o lib/api/schema.ts
check:
	.venv/bin/ruff check services/api scripts
	$(PY) scripts/check_contract.py
	cd apps/web && npm run typecheck
build:
	cd apps/web && npm run build
test-unit:
	.venv/bin/pytest -q services/api/tests/unit
test-graph:
	.venv/bin/pytest -q services/api/tests/integration
test-e2e:
	cd apps/web && npm run test:e2e
evaluate:
	$(PY) scripts/evaluate.py
smoke:
	$(PY) scripts/smoke.py
demo-reset:
	$(PY) scripts/reset.py

.env:
	python3 scripts/init_env.py
