# Task CRUD API

A simple REST API for managing a to-do list, built with **Python + FastAPI**.
Data is stored in a **SQLite database** (`tasks.db`) — no server, no setup, just a file.
Built for the **W3 · A1 assignment** (FlyRank backend programme).

---

## What changed from Assignment 1

In Assignment 1, tasks were stored in a Python list in memory.
Every time the server restarted, all data was lost.

In this assignment, tasks are stored in a **SQLite database file** (`tasks.db`).
Data now survives server restarts.

> The API endpoints, request bodies, and responses are **identical** to Assignment 1.
> Only the storage layer changed — the client never noticed.

---

## Why SQLite?

| Reason | Detail |
|--------|--------|
| **Zero setup** | No database server to install or run |
| **Single file** | The entire database is one file: `tasks.db` |
| **Built into Python** | Uses the `sqlite3` module — no extra packages |
| **Perfect for learning** | Same SQL you'll use with PostgreSQL later |

---

## Where is `tasks.db` stored?

The file is created automatically **next to `main.py`** the first time the server starts:

```
Task Crud Api/
├── main.py       ← API logic + SQL queries
├── tasks.db      ← SQLite database (auto-created, gitignored)
├── requirements.txt
└── README.md
```

`tasks.db` is listed in `.gitignore` — it is generated data, not source code.
Anyone who clones the repo gets a fresh database created automatically on first run.

---

## Installation

**Requirements:** Python 3.10 or higher.

```bash
# 1. Clone the repository
git clone https://github.com/Moaaz-yassen/task-crud-api.git
cd task-crud-api

# 2. (Recommended) create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to run

```bash
uvicorn main:app --reload
```

- Server starts on **http://localhost:8000**
- `tasks.db` is created automatically if it does not exist
- Three sample tasks are inserted automatically on the first run only
- Restarting the server **never duplicates** the sample data

---

## Endpoints

| Method | Path | Status codes | Description |
|--------|------|-------------|-------------|
| GET | `/` | 200 | API name and version |
| GET | `/health` | 200 | Liveness check |
| GET | `/tasks` | 200 | List all tasks from the database |
| GET | `/tasks/{id}` | 200, 404 | Get one task by id |
| POST | `/tasks` | 201, 400 | Create a new task |
| PUT | `/tasks/{id}` | 200, 400, 404 | Update a task's title and/or done |
| DELETE | `/tasks/{id}` | 204, 404 | Delete a task |

---

## Swagger UI

Open **http://localhost:8000/docs** to see all endpoints and test them interactively.

![Swagger UI](swagger.png)

---

## Database viewer — DB Browser for SQLite

Download **DB Browser for SQLite** (free): https://sqlitebrowser.org/dl/

Open `tasks.db` with it to browse and edit data visually.

> **Screenshot placeholder**
> Take a screenshot of DB Browser showing the tasks table and save it as `db-browser.png`.
> Then replace this line with: `![DB Browser](db-browser.png)`

---

## Example SQL queries

Run these in DB Browser → **Execute SQL** tab:

```sql
-- List every task
SELECT * FROM tasks;

-- Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- Count all tasks
SELECT COUNT(*) FROM tasks;

-- Mark every task as completed
UPDATE tasks SET done = 1;

-- Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
```

After running `UPDATE` or `DELETE`, click **"Write Changes"** in DB Browser,
then refresh **http://localhost:8000/tasks** — the API immediately reflects the changes.

---

## Example curl requests

```bash
# List all tasks
curl -i http://localhost:8000/tasks

# Create a task
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# Update a task
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task
curl -i -X DELETE http://localhost:8000/tasks/1
```

---

## Persistence — proved

1. Start the server: `uvicorn main:app --reload`
2. Create a task via `POST /tasks`
3. Stop the server: `Ctrl + C`
4. Start again: `uvicorn main:app --reload`
5. Run `GET /tasks` — the task is still there ✅

This is the key difference from Assignment 1: data now survives restarts.

---

## Git history

```
Stage 0: create SQLite database
Stage 1: database read endpoints
Stage 2: insert into database
Stage 3: update and delete with SQL
Stage 4: explored SQLite
Stage 5: database documentation
```

---

## Author

Built as the W3 · A1 assignment for the FlyRank backend programme.
