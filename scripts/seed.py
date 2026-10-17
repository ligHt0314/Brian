from app.graph.repository import Repository
from app.memory.store import Store
from app.ingestion.service import Ingestion
from app.config import settings

if __name__ == "__main__":
    results = Ingestion(Repository(), Store(settings.sqlite_path)).seed()
    failed = [r for r in results if r["status"] == "failed"]
    print(
        f"Processed {len(results)} source imports; {len(failed)} failed. Existing revisions were preserved."
    )
    if failed:
        for r in failed:
            print(r["source_id"], r["error"])
        raise SystemExit(1)
