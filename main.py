# ============================================================
#  Task CRUD API — built with FastAPI (Python)
#  Assignment: A3 — Auth Login & Protect
#  Run with:   uvicorn main:app --reload
# ============================================================

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

# Import the single shared repository instance.
# All database logic lives in repository.py — not here.
from repository import repo
from supabase_client import supabase
from auth import router as auth_router
from protected import public_router, protected_router


# ── Startup event ───────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs once when the server starts
    print("\n✅ Server running and connected to Supabase\n")
    yield
    # (nothing special on shutdown)


# ── App setup ───────────────────────────────────────────────
app = FastAPI(
    title="Task API",
    description="A simple CRUD API with Authentication via Supabase.",
    version="4.0",
    lifespan=lifespan,
)

# Register the auth routes (/auth/signup, /auth/login, /auth/logout)
app.include_router(auth_router)

# Register public and protected routes
app.include_router(public_router)
app.include_router(protected_router)



# ── Request body models ──────────────────────────────────────

# These are identical to A1 — the API contract has not changed.

class TaskCreate(BaseModel):
    """Body for POST /tasks — only title is required."""
    title: str

class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id} — both fields are optional."""
    title: Optional[str] = None
    done: Optional[bool] = None


# ════════════════════════════════════════════════════════════
#  Routes — identical HTTP behaviour to A1 and A2
#  The only change: repo.* calls instead of inline SQL/list ops
# ════════════════════════════════════════════════════════════

@app.get("/", summary="API info",
         description="Returns the API name, version, and available endpoint paths.")
def root():
    return {"name": "Task API", "version": "3.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check",
         description="Returns {'status': 'ok'} to confirm the server is alive.")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks",
         description="Returns all tasks from the PostgreSQL database.")
def list_tasks():
    """GET /tasks — delegates entirely to the repository."""
    return repo.get_all()


@app.get("/tasks/{task_id}", summary="Get a single task",
         description="Returns one task by id. Returns 404 if not found.")
def get_task(task_id: int):
    """GET /tasks/{id} — 200 with task, or 404."""
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a task",
          description="Creates a new task. title is required. Returns 201.")
def create_task(body: TaskCreate):
    """POST /tasks — 201 with new task, or 400 if title is empty."""
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    return repo.create(body.title.strip())


@app.put("/tasks/{task_id}", summary="Update a task",
         description="Updates title and/or done. Returns 404 or 400 when appropriate.")
def update_task(task_id: int, body: TaskUpdate):
    """PUT /tasks/{id} — 200 with updated task, 404, or 400."""
    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail="Provide at least one field: title or done")

    if body.title is not None and not body.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")

    task = repo.update(
        task_id,
        title=body.title.strip() if body.title is not None else None,
        done=body.done,
    )
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task",
            description="Deletes a task. Returns 204 on success, 404 if not found.")
def delete_task(task_id: int):
    """DELETE /tasks/{id} — 204 on success, 404 if not found."""
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Response(status_code=204)
