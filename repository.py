# ============================================================
#  repository.py — PostgreSQL Task Repository
#
#  This file contains ALL the database logic.
#  main.py calls these methods but knows nothing about SQL.
#  To switch databases later, you only change this file.
# ============================================================

from database import get_db


class TaskRepository:
    """
    Implements CRUD operations against a PostgreSQL database.
    The five methods below mirror the five API operations exactly.
    """

    # ── READ ─────────────────────────────────────────────────

    def get_all(self):
        """Return every task ordered by id."""
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
                rows = cur.fetchall()
            # Convert each tuple (id, title, done) into a dict
            return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]
        finally:
            conn.close()   # always close, even if an error occurs

    def get_by_id(self, task_id: int):
        """Return one task by id, or None if not found."""
        conn = get_db()
        try:
            with conn.cursor() as cur:
                # %s is the Postgres placeholder (prevents SQL injection)
                cur.execute(
                    "SELECT id, title, done FROM tasks WHERE id = %s",
                    (task_id,),
                )
                row = cur.fetchone()
            if row is None:
                return None
            return {"id": row[0], "title": row[1], "done": bool(row[2])}
        finally:
            conn.close()

    # ── CREATE ───────────────────────────────────────────────

    def create(self, title: str):
        """Insert a new task and return it with the auto-assigned id."""
        conn = get_db()
        try:
            with conn.cursor() as cur:
                # RETURNING id tells Postgres to send back the new id
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
                    (title, False),
                )
                new_id = cur.fetchone()[0]
            conn.commit()   # save to disk
            return {"id": new_id, "title": title, "done": False}
        finally:
            conn.close()

    # ── UPDATE ───────────────────────────────────────────────

    def update(self, task_id: int, title=None, done=None):
        """
        Update a task's title and/or done.
        Returns the updated task, or None if not found.
        """
        conn = get_db()
        try:
            with conn.cursor() as cur:
                # First fetch the current values
                cur.execute(
                    "SELECT id, title, done FROM tasks WHERE id = %s",
                    (task_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None

                # Use the new value if provided; keep the old value otherwise
                new_title = title if title is not None else row[1]
                new_done  = done  if done  is not None else bool(row[2])

                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
                    (new_title, new_done, task_id),
                )
            conn.commit()
            return {"id": task_id, "title": new_title, "done": new_done}
        finally:
            conn.close()

    # ── DELETE ───────────────────────────────────────────────

    def delete(self, task_id: int):
        """
        Delete a task by id.
        Returns True on success, False if the task was not found.
        """
        conn = get_db()
        try:
            with conn.cursor() as cur:
                # Check it exists first so we can return the right status
                cur.execute(
                    "SELECT id FROM tasks WHERE id = %s",
                    (task_id,),
                )
                if cur.fetchone() is None:
                    return False

                cur.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,),
                )
            conn.commit()
            return True
        finally:
            conn.close()


# ── Single shared instance ────────────────────────────────────
# main.py imports this object and calls its methods.
repo = TaskRepository()
