# ============================================================
#  auth.py — Authentication routes
#  POST /auth/signup
#  POST /auth/login
#  POST /auth/logout  (added in Stage 4)
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from supabase_client import supabase
from dependencies import get_current_user
from supabase_client import supabase

# APIRouter lets us group related routes and include them in main.py
router = APIRouter(prefix="/auth", tags=["Auth"])


# ── Request body models ──────────────────────────────────────

class AuthBody(BaseModel):
    """Body for signup and login — both need email and password."""
    email: str
    password: str


# ════════════════════════════════════════════════════════════
#  STAGE 1 — Sign Up
# ════════════════════════════════════════════════════════════

@router.post("/signup", status_code=201, summary="Create a new user account")
def signup(body: AuthBody):
    """
    POST /auth/signup

    Registers a new user with Supabase Auth.
    - Missing email or password → 400
    - Supabase error (e.g. email already used) → 400
    - Success → 201 with user object
    """
    # Validate: both fields must be non-empty
    if not body.email.strip() or not body.password.strip():
        raise HTTPException(status_code=400, detail="email and password are required")

    try:
        # Call Supabase Auth to register the user
        response = supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
        })
    except Exception as e:
        # Catch any Supabase/network error and return 400
        raise HTTPException(status_code=400, detail=str(e))

    if response.user is None:
        raise HTTPException(status_code=400, detail="Signup failed. Email may already be in use.")

    return {
        "message": "Account created successfully",
        "user": {
            "id":    str(response.user.id),
            "email": response.user.email,
        },
    }


# ════════════════════════════════════════════════════════════
#  STAGE 1 — Log In
# ════════════════════════════════════════════════════════════

@router.post("/login", summary="Authenticate and receive a JWT token")
def login(body: AuthBody):
    """
    POST /auth/login

    Authenticates an existing user.
    - Missing fields → 400
    - Wrong credentials → 401
    - Success → 200 with access_token and refresh_token
    """
    # Validate inputs
    if not body.email.strip() or not body.password.strip():
        raise HTTPException(status_code=400, detail="email and password are required")

    try:
        # supabase.auth.sign_in_with_password() verifies credentials
        # and returns a session containing the JWT tokens
        response = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })
    except Exception:
        # Supabase raises an exception for wrong password / unknown email
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    if response.session is None:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token":  response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "token_type":    "bearer",
    }


# ════════════════════════════════════════════════════════════
#  STAGE 4 — Log Out
# ════════════════════════════════════════════════════════════

@router.post("/logout", status_code=204, summary="Log out the current user")
def logout(user = Depends(get_current_user)):
    """
    POST /auth/logout

    Logs the user out. Requires a valid Bearer token.
    Returns 204 No Content on success.
    """
    try:
        # Sign out from Supabase (clears the session)
        supabase.auth.sign_out()
    except Exception:
        pass
    
    return

