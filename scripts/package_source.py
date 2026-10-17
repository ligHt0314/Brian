"""Package reproducible source and synthetic media, excluding all runtime secrets/state."""

import os
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
roots = ["apps", "services", "fixtures", "docs", "scripts", "infra", "tests", "evals"]
exclude = {
    ".git",
    ".venv",
    ".data",
    "node_modules",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "test-results",
    "playwright-report",
}
files = []
for name in roots:
    for folder, dirs, names in os.walk(root / name):
        dirs[:] = [d for d in dirs if d not in exclude]
        files.extend(
            Path(folder) / n
            for n in names
            if n != ".env" and not n.endswith((".pyc", ".tsbuildinfo", ".DS_Store"))
        )
files.extend(
    p
    for p in root.iterdir()
    if p.is_file()
    and (
        p.suffix == ".md"
        or p.name
        in {
            "Makefile",
            "pyproject.toml",
            "uv.lock",
            "requirements.lock",
            "compose.yaml",
            "compose.dev.yaml",
            ".env.example",
            ".gitignore",
            ".dockerignore",
        }
    )
)
files.extend(
    root / "artifacts" / n
    for n in [
        "persistence.json",
        "gemini-live-verification.json",
        "workspace-home-desktop.png",
        "workspace-home-mobile.png",
        "workspace-guide-desktop.png",
        "workspace-guide-mobile.png",
        "workspace-investigation-desktop.png",
        "workspace-updated-desktop.png",
    ]
    if (root / "artifacts" / n).exists()
)
target = root / "artifacts/company-brain-source.zip"
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(set(files)):
        archive.write(file, "company-brain/" + str(file.relative_to(root)))
with zipfile.ZipFile(target) as archive:
    names = archive.namelist()
    assert not any(name.endswith("/.env") or "/node_modules/" in name or "/.data/" in name for name in names)
print(
    f"Packaged {len(names)} files; {target.stat().st_size} bytes. Runtime credentials, databases and dependencies excluded."
)
