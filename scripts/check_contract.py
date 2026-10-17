import json
import subprocess
import tempfile
from pathlib import Path
from app.main import app

root = Path(__file__).resolve().parents[1]
path = root / "apps/web/lib/api/openapi.json"
assert json.loads(path.read_text()) == app.openapi(), "OpenAPI changed; run make contract"
with tempfile.TemporaryDirectory() as tmp:
    target = Path(tmp) / "schema.ts"
    subprocess.run(
        [str(root / "apps/web/node_modules/.bin/openapi-typescript"), str(path), "-o", str(target)],
        check=True,
        capture_output=True,
    )
    assert target.read_text() == (root / "apps/web/lib/api/schema.ts").read_text(), (
        "Generated TypeScript changed; run make contract"
    )
print("API schema and generated TypeScript are synchronized")
