import secrets
import pytest
from fastapi.testclient import TestClient
from app.config import settings
from app.graph.repository import Repository
from app.memory.store import Store
from app.ingestion.service import Ingestion
from app.main import app
import app.main as main


@pytest.fixture
def world(tmp_path, monkeypatch):
    # Ordinary regression tests never consume configured provider credits.
    monkeypatch.setattr(settings, "llm_api_key", "")
    repo = Repository("company_brain_test_" + secrets.token_hex(8))
    store = Store(str(tmp_path / "operations.sqlite"))
    ingestion = Ingestion(repo, store)
    ingestion.seed()
    monkeypatch.setattr(main, "repo", repo)
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(main, "ingestion", ingestion)
    with TestClient(app, headers={"origin": "http://localhost:3000", "x-brain-csrf": "1"}) as client:
        yield repo, store, ingestion, client
    repo.graph.delete()
    store.db.close()


def login(client, persona="Engineer"):
    assert client.post("/api/v1/demo/session", json={"persona": persona}).status_code == 200


def ask(client, question, **kw):
    session = client.post("/api/v1/sessions").json()["id"]
    response = client.post("/api/v1/investigations", json={"session_id": session, "question": question, **kw})
    assert response.status_code == 200, response.text
    result = client.get("/api/v1/investigations/" + response.json()["run_id"])
    assert result.status_code == 200, result.text
    assert result.json()["status"] == "complete", result.text
    return result.json()
