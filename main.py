# ============================================================
#  Task CRUD API — built with FastAPI (Python)
#  Assignment: W2 · A1
#  Run with:  uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI

# FastAPI() creates our application.
# The title and description appear on the Swagger page at /docs.
app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks. Built for the W2·A1 assignment.",
    version="1.0",
)


# ════════════════════════════════════════════════════════════
#  STAGE 1 — Root and health endpoints
# ════════════════════════════════════════════════════════════

@app.get(
    "/",
    summary="API info",
    description="Returns the API name, version, and available endpoint paths.",
)
def root():
    """GET / — describes this API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get(
    "/health",
    summary="Health check",
    description="Returns {'status': 'ok'} so a monitoring tool can confirm the server is alive.",
)
def health():
    """GET /health — quick liveness check."""
    return {"status": "ok"}
