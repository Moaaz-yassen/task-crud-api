# ============================================================
#  dependencies.py — Reusable auth dependencies (Stage 4)
# ============================================================

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase_client import supabase

# HTTPBearer tells FastAPI (and Swagger UI) that this endpoint
# requires an "Authorization: Bearer <token>" header.
# This automatically adds the "Authorize" 🔒 button in Swagger!
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Dependency that extracts the JWT token from the Authorization header,
    verifies it with Supabase, and returns the authenticated user object.
    If the token is missing or invalid, it throws a 401 error.
    """
    token = credentials.credentials

    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        # Supabase throws an error if the token is forged or expired
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if user_response.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Return the secure user object so the route can use it
    return user_response.user
