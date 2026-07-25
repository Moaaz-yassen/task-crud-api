# Task CRUD API

A simple REST API for managing a to-do list, built with **Python + FastAPI**.
Data is stored in **PostgreSQL**, running in **Docker**.
The entire stack starts with a single command: `docker compose up`.

Built for the **FlyRank backend programme** (Assignments A1 → A2 → A3).

---

## Assignment history

| Assignment | Storage | Run command |
|-----------|---------|-------------|
| A1 | Python list (in-memory) | `uvicorn main:app --reload` |
| A2 (W3·A1) | SQLite file (`tasks.db`) | `uvicorn main:app --reload` |
| **A3 (current)** | **PostgreSQL in Docker** | **`docker compose up`** |

> The API endpoints, request bodies, responses, and status codes are **identical** across all three assignments.
> Only the storage layer changed — the client never noticed.

---

## Architecture

```
docker compose up
      │
      ├── db  (postgres:16, port 5432)
      │    ├── volume: postgres_data  ← data survives restarts
      │    └── init.sql               ← creates table + 3 seed tasks on first boot
      │
      └── app (FastAPI, port 8000)
           ├── main.py        ← routes (unchanged from A1)
           ├── repository.py  ← all SQL queries live here
           └── database.py    ← reads DATABASE_URL from .env
```

### Why repository pattern?

`main.py` routes call `repo.get_all()`, `repo.create()`, etc.
`repository.py` is the **only** file that knows PostgreSQL exists.
To switch to a different database, only `repository.py` changes — routes stay untouched.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (free) — must be running

---

## Environment variables

Copy `.env.example` to `.env` before running:

```bash
cp .env.example .env      # Mac / Linux
copy .env.example .env    # Windows
```

| Variable | Example value | Description |
|----------|--------------|-------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@db:5432/taskdb` | Postgres connection string |

> `.env` is listed in `.gitignore` — it is never committed.
> `.env.example` is committed so anyone can clone and run immediately.

---

## How to run

```bash
docker compose up
```

That's it. Docker will:
1. Pull the `postgres:16` image
2. Build the FastAPI app image
3. Start Postgres, wait for it to be ready
4. Start the FastAPI app
5. Create the `tasks` table and insert 3 seed tasks (first run only)

Open **http://localhost:8000/docs** to see the Swagger UI.

To stop:
```bash
docker compose down        # stops containers, keeps data
docker compose down -v     # stops containers AND deletes all data
```

To rebuild after code changes:
```bash
docker compose up --build
```

---

## Endpoints

| Method | Path | Status codes | Description |
|--------|------|-------------|-------------|
| GET | `/` | 200 | API name and version |
| GET | `/health` | 200 | Liveness check |
| GET | `/tasks` | 200 | List all tasks |
| GET | `/tasks/{id}` | 200, 404 | Get one task by id |
| POST | `/tasks` | 201, 400 | Create a new task |
| PUT | `/tasks/{id}` | 200, 400, 404 | Update a task |
| DELETE | `/tasks/{id}` | 204, 404 | Delete a task |

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

## Persistence — how it was verified

1. `docker compose up` — server started, 3 seed tasks visible at `GET /tasks`
2. `POST /tasks` with `{"title": "Test persistence"}` — new task created (id = 4)
3. `docker compose down` — containers stopped
4. `docker compose up` — containers restarted
5. `GET /tasks` — all 4 tasks still present ✅

The data survives because PostgreSQL stores it in the `postgres_data` Docker volume,
not inside the container itself. Volumes are not deleted by `docker compose down`.

---

## Swagger UI

Open **http://localhost:8000/docs** after running `docker compose up`.

![Swagger UI](swagger.png)

---

## Project structure

```
Task Crud Api/
├── main.py             ← API routes (unchanged from A1)
├── repository.py       ← all PostgreSQL queries
├── database.py         ← connection helper (reads from .env)
├── init.sql            ← creates table + seeds data on first Postgres boot
├── Dockerfile          ← builds the FastAPI app container
├── docker-compose.yml  ← starts app + db with one command
├── .env                ← your connection string (gitignored)
├── .env.example        ← template (committed)
├── requirements.txt
└── README.md
```

---

## Git history

```
Stage 0: hello server                        (A1)
Stage 1: root and health endpoints           (A1)
Stage 2: read endpoints with 404             (A1)
Stage 3: create with validation              (A1)
Stage 4: full CRUD                           (A1)
Stage 5: Swagger UI                          (A1)
Stage 6: publish and docs                    (A1)
Stage 0: create SQLite database              (W3·A1)
Stage 1: database read endpoints             (W3·A1)
Stage 2: insert into database                (W3·A1)
Stage 3: update and delete with SQL          (W3·A1)
Stage 4: explored SQLite                     (W3·A1)
Stage 5: database documentation              (W3·A1)
A2 Stage 1: swap SQLite for Postgres repository
A2 Stage 2: add init.sql for table creation
A2 Stage 3: add Dockerfile and docker-compose
A2 Stage 4: update README for PostgreSQL and Docker
```
