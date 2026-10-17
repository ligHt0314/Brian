"""Create local configuration once. Never print generated secrets."""

from pathlib import Path
import secrets

root = Path(__file__).resolve().parents[1]
path = root / ".env"
if path.exists():
    print("Existing .env preserved.")
else:
    content = (root / ".env.example").read_text()
    content = content.replace(
        "replace-with-a-random-secret-at-least-32-characters", secrets.token_urlsafe(48)
    )
    content = content.replace("OPERATOR_RESET_TOKEN=", "OPERATOR_RESET_TOKEN=" + secrets.token_urlsafe(32))
    path.write_text(content)
    path.chmod(0o600)
    print("Created private .env with new local demo secrets. No model key configured.")
