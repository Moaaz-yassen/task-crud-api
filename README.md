# Task CRUD API

A simple REST API for managing a to-do list, built with **Python + FastAPI**.  
All data is stored **in memory** — no database, no files.  
Built as the **W2 · A1 assignment** for the FlyRank backend programme.

---

## What this is

This API lets any HTTP client (browser, curl, Swagger UI, a mobile app) create, read, update and delete tasks.  
It demonstrates the four **CRUD** operations mapped onto HTTP methods:

| CRUD | HTTP method | Endpoint |
|------|-------------|----------|
| Create | POST | `POST /tasks` |
| Read | GET | `GET /tasks` · `GET /tasks/{id}` |
| Update | PUT | `PUT /tasks/{id}` |
| Delete | DELETE | `DELETE /tasks/{id}` |

---

## Installation

**Requirements:** Python 3.10 or higher.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. (Optional but recommended) create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Run the server

```bash
uvicorn main:app --reload
```

The server starts on **http://localhost:8000**.  
`--reload` restarts automatically when you edit `main.py`.

---

## Endpoints

| Method | Path | Status codes | Description |
|--------|------|-------------|-------------|
| GET | `/` | 200 | API name, version and available paths |
| GET | `/health` | 200 | Liveness check — returns `{"status": "ok"}` |
| GET | `/tasks` | 200 | List all tasks |
| GET | `/tasks/{id}` | 200, 404 | Get one task by id |
| POST | `/tasks` | 201, 400 | Create a new task |
| PUT | `/tasks/{id}` | 200, 400, 404 | Update a task's title and/or done |
| DELETE | `/tasks/{id}` | 204, 404 | Delete a task |

---

## Swagger UI (interactive docs)

FastAPI generates interactive documentation automatically.  
Open **http://localhost:8000/docs** in your browser to see all endpoints and use the **"Try it out"** button to test them without curl.

> **Screenshot placeholder**  
> After running the server, take a screenshot of http://localhost:8000/docs and save it as `swagger.png` in the root of this repo. Then replace this line with:  
> `![Swagger UI](swagger.png)`

---

## Example curl requests

### Create a task (POST)
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

**Expected output:**
```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

### List all tasks (GET)
```bash
curl -i http://localhost:8000/tasks
```

### Get one task (GET)
```bash
curl -i http://localhost:8000/tasks/1
```

### Update a task (PUT)
```bash
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Delete a task (DELETE)
```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```
*(Returns 204 No Content — empty body, which means success.)*

### Trigger a 404
```bash
curl -i http://localhost:8000/tasks/99
```

### Trigger a 400 (missing title)
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## Status codes used

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET or PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Missing or empty `title` |
| 404 | Not Found | No task with that id |

---

## Project structure

```
Task Crud Api/
├── main.py           # All API logic — one file, heavily commented
├── requirements.txt  # Python dependencies
├── .gitignore        # Ignores __pycache__, .venv, etc.
└── README.md         # This file
```

---

## In-memory storage — a note

Tasks exist only while the server is running. Restart it and the list resets to the three seed tasks. This is intentional for this assignment — a real database (coming next week) exists to solve exactly this problem.

---

## Git history

```
Stage 0: hello server
Stage 1: root and health endpoints
Stage 2: read endpoints with 404
Stage 3: create with validation
Stage 4: full CRUD
Stage 5: Swagger UI
Stage 6: publish and docs
```
