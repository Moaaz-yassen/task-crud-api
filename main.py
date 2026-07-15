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


# ── Hello endpoint ───────────────────────────────────────────
# This is our very first endpoint. It proves the server is alive.
@app.get("/")
def root():
    """GET / — hello message so we can confirm the server works."""
    return {"message": "Hello from Task API!"}
