"""Reversible, one-time Orbit -> BrightMart replacement. Run with the API stopped.
Retires only the exact old synthetic graph and preserves its uploads and operational history.
"""

import argparse
import json
from app.config import settings
from app.graph.repository import Repository
from app.ingestion.service import Ingestion, FIXTURES
from app.memory.store import Store

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--replace-orbit", action="store_true", required=True)
parser.parse_args()
if not settings.demo_mode or settings.falkordb_graph != "company_brain_brightmart_demo":
    raise SystemExit("Replacement requires the exact configured synthetic BrightMart graph.")
repo = Repository()
store = Store(settings.sqlite_path)
manifest = json.loads((FIXTURES / "manifest.json").read_text())
results = Ingestion(repo, store).seed()
if any(r["status"] != "complete" for r in results):
    raise SystemExit("BrightMart import failed. Old graph was preserved.")
sources = repo.sources(["all_employees", "engineering", "leadership"])
claims, truncated = repo.claims([s["id"] for s in sources])
if len(sources) != manifest["source_count"] or len(claims) != manifest["claim_count"] or truncated:
    raise SystemExit("BrightMart counts did not match. Old graph was preserved.")
old_name = "company_brain_orbit_demo"
archive_name = "retired_company_brain_orbit_demo_20261017"
connection = repo.db.connection
graphs = connection.execute_command("GRAPH.LIST")
if old_name in graphs:
    if archive_name in graphs:
        raise SystemExit("Archive already exists; refused to overwrite it.")
    connection.execute_command("RENAME", old_name, archive_name)
with store.lock, store.db:
    archived = store.db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='retired_orbit_records_20261017'"
    ).fetchone()
    if not archived:
        store.db.execute("ALTER TABLE records RENAME TO retired_orbit_records_20261017")
        store.db.execute(
            "CREATE TABLE records (id TEXT PRIMARY KEY, kind TEXT, actor TEXT, data TEXT, created_at TEXT)"
        )
store.db.close()
print(
    json.dumps(
        {
            "company": "BrightMart",
            "sources": len(sources),
            "claims": len(claims),
            "old_dataset_active": old_name in connection.execute_command("GRAPH.LIST"),
            "retired_graph_archive": archive_name,
            "history": "preserved in retired_orbit_records_20261017; active history starts empty",
            "original_uploads": "preserved",
        }
    )
)
