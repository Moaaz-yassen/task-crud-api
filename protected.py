# ============================================================
#  protected.py — Public and Protected route endpoints
#
#  GET /public/info       — no auth required
#  GET /protected/profile — auth required (verified in Stage 3)
# ============================================================

from fastapi import APIRouter, HTTPException, Request

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
#  STAGE 2 — Protected endpoint (token extracted but not yet verified)
#  Token verification is added in Stage 3.
# ════════════════════════════════════════════════════════════

@protected_router.get("/profile", summary="Private profile — Bearer token required")
def profile(request: Request):
    """
    GET /protected/profile

    Stage 2: checks that the Authorization header exists and has the right format.
    Stage 3: will also verify the token with Supabase.

    Authorization header format:
        Authorization: Bearer <your_jwt_token>
    """
    # Extract the Authorization header
    auth_header = request.headers.get("Authorization")

    # If the header is missing entirely → 401
    if not auth_header:
        raise HTTPException(status_code=401, detail="Access token required")

    # The header must start with "Bearer " followed by the token
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        raise HTTPException(status_code=401, detail="Access token required")

    token = parts[1]

    # ── Stage 3 will verify the token here ──
    # For now, just confirm the header was present and formatted correctly.
    return {"message": "Token received — verification coming in Stage 3", "token_preview": token[:20] + "..."}
