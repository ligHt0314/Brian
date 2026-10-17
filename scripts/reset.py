import os
import httpx

token = os.environ.get("OPERATOR_RESET_TOKEN", "")
if not token:
    raise SystemExit(
        "Set OPERATOR_RESET_TOKEN in the server environment and this shell. Reset is operator-only."
    )
with httpx.Client(
    base_url=os.environ.get("BRAIN_API_URL", "http://127.0.0.1:8000"),
    headers={"origin": "http://localhost:3000", "x-brain-csrf": "1"},
) as client:
    client.post("/api/v1/demo/session", json={"persona": "Lead"}).raise_for_status()
    r = client.post("/api/v1/demo/reset", headers={"x-operator-token": token})
    r.raise_for_status()
    print(r.json()["status"])
