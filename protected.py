# ============================================================
#  protected.py — Public and Protected route endpoints
#
#  GET /public/info       — no auth required
#  GET /protected/profile — auth required (verified in Stage 3)
# ============================================================

from fastapi import APIRouter, Depends
from dependencies import get_current_user

# Two separate routers — one for public, one for protected
public_router    = APIRouter(prefix="/public",    tags=["Public"])
protected_router = APIRouter(prefix="/protected", tags=["Protected"])


# ════════════════════════════════════════════════════════════
#  STAGE 2 — Public endpoint (no token needed)
# ════════════════════════════════════════════════════════════

@public_router.get("/info", summary="Public information — no auth required")
def public_info():
    """
    GET /public/info

    Anyone can call this — no Authorization header needed.
    Always returns 200.
    """
    return {"message": "Welcome stranger! This info is public."}


# ════════════════════════════════════════════════════════════
#  STAGE 4 — Protected endpoint using reusable middleware
# ════════════════════════════════════════════════════════════

@protected_router.get("/profile", summary="Private profile — Bearer token required")
def profile(user = Depends(get_current_user)):
    """
    GET /protected/profile

    This endpoint is protected by the `get_current_user` dependency (middleware).
    The route logic only runs if the user is successfully authenticated.
    """
    # Verification successful! Return the secure user metadata.
    return {
        "message": "Token verified successfully!",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "created_at": str(user.created_at)
        }
    }

