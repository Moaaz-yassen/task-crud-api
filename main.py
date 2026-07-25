# ============================================================
#  Task CRUD API — built with FastAPI (Python)
#  Assignment: W3 · A1 — Connecting your CRUD to the database
#  Run with:  uvicorn main:app --reload
# ============================================================

import sqlite3                          # built into Python — no install needed
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

# ── App setup ───────────────────────────────────────────────
app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks. Data is stored in SQLite.",
    version="2.0",
)


# ════════════════════════════════════════════════════════════
#  STAGE 0 — SQLite database setup
# ════════════════════════════════════════════════════════════

# The database lives in a single file next to main.py.
# SQLite creates this file automatically the first time the app runs.
DB_PATH = "tasks.db"


def get_db():
    """
    Open and return a connection to tasks.db.

    row_factory = sqlite3.Row lets us access columns by name
    (e.g. row["title"]) instead of by index (row[1]).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Run once at startup:
      1. Create the tasks table if it does not already exist.
      2. Insert three sample tasks ONLY if the table is empty.

    This means restarting the server never duplicates data.
    """
    conn = get_db()
    cur = conn.cursor()

    # CREATE TABLE IF NOT EXISTS means this is completely safe to run
    # on every restart — it does nothing if the table already exists.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Only seed sample data when the table is brand new (empty).
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]   # fetchone()[0] is the integer count

    if count == 0:
        # executemany inserts all three rows in one call
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy groceries", False),
                ("Walk the dog",  False),
                ("Read a book",   True),
            ],
        )

    conn.commit()   # save everything to disk
    conn.close()


# Call init_db() immediately when the module loads.
# This runs before any request is handled.
init_db()


# ── Request body models ──────────────────────────────────────
# (unchanged from A1)

class TaskCreate(BaseModel):
    """Body for POST /tasks — only title is required."""
    title: str

class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id} — both fields are optional."""
    title: Optional[str] = None
    done: Optional[bool] = None


# ── Helper (still used by the in-memory routes below) ────────
def find_task(task_id: int):
    """Return the task dict with the given id, or None."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# ── In-memory list (temporary — will be removed in Stage 1–3) ─
# Keeping this so the API keeps working while we migrate stage by stage.
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog",  "done": False},
    {"id": 3, "title": "Read a book",   "done": True},
]
next_id = 4


# ════════════════════════════════════════════════════════════
#  API Routes (unchanged from A1)
# ════════════════════════════════════════════════════════════

@app.get("/", summary="API info",
         description="Returns the API name, version, and available endpoint paths.")
def root():
    return {"name": "Task API", "version": "2.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check",
         description="Returns {'status': 'ok'} to confirm the server is alive.")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks",
         description="Returns all tasks.")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get a single task",
         description="Returns one task by id. Returns 404 if not found.")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a task",
          description="Creates a new task. title is required. Returns 201.")
def create_task(body: TaskCreate):
    global next_id
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    new_task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task",
         description="Updates title and/or done. Returns 404 or 400 when appropriate.")
def update_task(task_id: int, body: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail="Provide at least one field: title or done")
    if body.title is not None:
        if not body.title.strip():
            raise HTTPException(status_code=400, detail="title cannot be empty")
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task",
            description="Deletes a task. Returns 204 on success, 404 if not found.")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return Response(status_code=204)
