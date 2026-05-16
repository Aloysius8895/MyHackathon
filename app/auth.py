from fastapi import Depends, Header, HTTPException, status

from app.config import Settings, get_settings
from app.models import AuthContext


def initialize_firebase_auth(settings: Settings) -> None:
    try:
        import firebase_admin
    except ImportError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="firebase-admin is not installed") from exc

    if firebase_admin._apps:
        return

    options = {"projectId": settings.firebase_project_id} if settings.firebase_project_id else None
    try:
        firebase_admin.initialize_app(options=options)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Firebase Admin could not initialize") from exc


async def get_auth_context(
    authorization: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> AuthContext:
    if settings.auth_mode == "disabled":
        return AuthContext(user_id="local-admin", role="admin")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Firebase bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    initialize_firebase_auth(settings)
    try:
        from firebase_admin import auth
    except ImportError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="firebase-admin is not installed") from exc

    try:
        claims = auth.verify_id_token(token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token") from exc

    role = claims.get("role") or claims.get("admin_role") or "user"
    return AuthContext(user_id=claims["uid"], role=role, claims=claims)


def require_admin(auth_context: AuthContext = Depends(get_auth_context)) -> AuthContext:
    if auth_context.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return auth_context
