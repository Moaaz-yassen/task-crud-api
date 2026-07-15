# ============================================================
#  Task CRUD API — built with FastAPI (Python)
#  Assignment: W2 · A1
#  Run with:  uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI() creates our application.
# The title and description appear on the Swagger page at /docs.
app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks. Built for the W2·A1 assignment.",
    version="1.0",
)


# ── In-memory "database" ─────────────────────────────────────
# This is just a Python list. All tasks live here while the
# server is running. Restarting the server wipes this list —
# that's intentional; a real database fixes that (next week).
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog",  "done": False},
    {"id": 3, "title": "Read a book",   "done": True},
]

# We use a counter to give every new task a unique id.
# Starting at 4 because our three seed tasks already used 1–3.
next_id = 4


# ── Request body models ──────────────────────────────────────
# Pydantic models describe what JSON the client must send.
# FastAPI validates the incoming JSON automatically against them.

class TaskCreate(BaseModel):
    """Body for POST /tasks — only title is required."""
    title: str  # required field


# ── Helper ───────────────────────────────────────────────────
def find_task(task_id: int):
    """Return the task dict with the given id, or None."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


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


# ════════════════════════════════════════════════════════════
#  STAGE 2 — Read: list all tasks and get one task
# ════════════════════════════════════════════════════════════

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns the full list of tasks currently in memory.",
)
def list_tasks():
    """GET /tasks — returns all tasks (200 OK)."""
    return tasks


@app.get(
    "/tasks/{task_id}",
    summary="Get a single task",
    description="Returns one task by its id. Returns 404 if no task has that id.",
)
def get_task(task_id: int):
    """GET /tasks/{id} — returns one task (200) or 404."""
    task = find_task(task_id)
    if task is None:
        # 404 means "the thing you asked for does not exist"
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ════════════════════════════════════════════════════════════
#  STAGE 3 — Create: POST a new task
# ════════════════════════════════════════════════════════════

@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task. Body must include a non-empty `title`. Returns 201 with the created task.",
)
def create_task(body: TaskCreate):
    """POST /tasks — creates a task (201) or 400 if title is missing/empty."""
    global next_id  # we need to modify the module-level counter

    # Validate: title must not be blank (FastAPI already ensures it's a string,
    # but we also reject empty strings like "   ")
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    # Build the new task and append it to our in-memory list
    new_task = {
        "id": next_id,
        "title": body.title.strip(),
        "done": False,
    }
    tasks.append(new_task)
    next_id += 1  # increment so the next task gets a different id

    return new_task
