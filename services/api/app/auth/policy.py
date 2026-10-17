from fastapi import HTTPException, Request
from itsdangerous import URLSafeTimedSerializer, BadSignature
from app.domain.models import Me
from app.config import settings

PERSONAS = {
    "Engineer": Me(
        id="demo_engineer",
        persona="Engineer",
        groups=["all_employees", "engineering"],
        capabilities=["investigate", "review"],
    ),
    "Lead": Me(
        id="demo_lead",
        persona="Lead",
        groups=["all_employees", "engineering", "leadership"],
        capabilities=["investigate", "review", "import"],
    ),
    "Viewer": Me(id="demo_viewer", persona="Viewer", groups=["all_employees"], capabilities=["investigate"]),
}
serializer = URLSafeTimedSerializer(settings.session_secret, salt="company-brain-session-v1")


def current_user(request: Request) -> Me:
    try:
        persona = serializer.loads(request.cookies.get("brain_session", ""), max_age=86400)
        return PERSONAS[persona]
    except (BadSignature, KeyError):
        raise HTTPException(401, "Choose a workspace role to continue")


def require(user: Me, capability: str):
    if capability not in user.capabilities:
        raise HTTPException(403, "This action is unavailable to this identity")


def unavailable():
    raise HTTPException(404, "This record is unavailable")
