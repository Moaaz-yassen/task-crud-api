# ============================================================
#  Task CRUD API — built with FastAPI (Python)
#  Assignment: W3 · A1 — Connecting your CRUD to the database
#  Run with:  uvicorn main:app --reload
# ============================================================

import sqlite3
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
#  Database helpers
# ════════════════════════════════════════════════════════════

DB_PATH = "tasks.db"


def get_db():
    """Open and return a connection to tasks.db."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # access columns by name: row["title"]
    return conn


def init_db():
    """
    Run once at startup:
      1. Create the tasks table if it does not already exist.
      2. Insert three sample tasks ONLY if the table is empty.
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Seed only when the table is brand new (empty)
    cur.execute("SELECT COUNT(*) FROM tasks")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy groceries", False),
                ("Walk the dog",  False),
                ("Read a book",   True),
            ],
        )

    conn.commit()
    conn.close()


# Run on every startup — safe to call repeatedly
init_db()


# ── Helper: convert a sqlite3.Row to a plain dict ───────────
def row_to_dict(row):
    """
    sqlite3.Row behaves like a dict but FastAPI needs a real dict.
    We also convert done from 0/1 (SQLite stores booleans as integers)
    back to Python True/False so the JSON looks correct.
    """
    return {
        "id":    row["id"],
        "title": row["title"],
        "done":  bool(row["done"]),   # 0 → False, 1 → True
    }


# ── Request body models ──────────────────────────────────────

class TaskCreate(BaseModel):
    """Body for POST /tasks — only title is required."""
    title: str

class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id} — both fields are optional."""
    title: Optional[str] = None
    done: Optional[bool] = None


# ════════════════════════════════════════════════════════════
#  Routes
# ════════════════════════════════════════════════════════════

@app.get("/", summary="API info",
         description="Returns the API name, version, and available endpoint paths.")
def root():
    return {"name": "Task API", "version": "2.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check",
         description="Returns {'status': 'ok'} to confirm the server is alive.")
def health():
    return {"status": "ok"}


# ── STAGE 1 — Read endpoints now use SQL ─────────────────────

@app.get("/tasks", summary="List all tasks",
         description="Returns all tasks from the SQLite database.")
def list_tasks():
    """
    GET /tasks — SQL: SELECT * FROM tasks

    Opens the database, runs a SELECT, converts every row to a dict,
    and returns the list. No other change from A1.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
    rows = cur.fetchall()          # list of sqlite3.Row objects
    conn.close()
    return [row_to_dict(r) for r in rows]   # convert to list of dicts


@app.get("/tasks/{task_id}", summary="Get a single task",
         description="Returns one task by id. Returns 404 if not found.")
def get_task(task_id: int):
    """
    GET /tasks/{id} — SQL: SELECT * FROM tasks WHERE id = ?

    The ? is a placeholder — sqlite3 fills it in safely (prevents SQL injection).
    If no row is found, we raise 404 exactly like before.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()           # one row or None
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return row_to_dict(row)


# ── STAGE 2 (coming next) — POST still uses in-memory for now ─

@app.post("/tasks", status_code=201, summary="Create a task",
          description="Creates a new task. title is required. Returns 201.")
def create_task(body: TaskCreate):
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    conn = get_db()
    cur = conn.cursor()
    # INSERT and let SQLite auto-assign the id
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (body.title.strip(), False),
    )
    conn.commit()
    new_id = cur.lastrowid     # SQLite tells us the id it just assigned
    conn.close()

    return {"id": new_id, "title": body.title.strip(), "done": False}


@app.put("/tasks/{task_id}", summary="Update a task",
         description="Updates title and/or done. Returns 404 or 400 when appropriate.")
def update_task(task_id: int, body: TaskUpdate):
    # Check the task exists first
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if body.title is None and body.done is None:
        conn.close()
        raise HTTPException(status_code=400, detail="Provide at least one field: title or done")

    # Build updated values (keep existing if not provided)
    new_title = body.title.strip() if body.title is not None else row["title"]
    new_done  = body.done          if body.done  is not None else bool(row["done"])

    if body.title is not None and not new_title:
        conn.close()
        raise HTTPException(status_code=400, detail="title cannot be empty")

    cur.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, task_id),
    )
    conn.commit()
    conn.close()

    return {"id": task_id, "title": new_title, "done": new_done}


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task",
            description="Deletes a task. Returns 204 on success, 404 if not found.")
def delete_task(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return Response(status_code=204)
