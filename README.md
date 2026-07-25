```markdown
# Task API

A CRUD API for managing a to-do list, built with FastAPI and backed by a SQLite database. Data persists across server restarts.

## Why SQLite

SQLite was chosen because it requires no separate database server — the entire database lives in a single file (`tasks.db`) that's created automatically the first time the app runs. This makes it ideal for learning and small projects: zero setup, zero configuration, and easy to inspect directly with a tool like DB Browser for SQLite.

## Database

- **File:** `tasks.db`, created automatically in the project root on first run
- **Table:** `tasks` (`id` autoincrementing primary key, `title` text, `done` boolean)
- Three example tasks are seeded automatically the first time the table is empty
- Data survives server restarts — only wiped if `tasks.db` is deleted manually

## Setup & Run

1. Clone this repo
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/Scripts/activate   # Windows Git Bash
   source venv/bin/activate       # Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install fastapi uvicorn
   ```
4. Run the server:
   ```
   uvicorn main:app --reload --port 8000
   ```
5. Visit `http://127.0.0.1:8000/docs` for interactive API docs.

The database file (`tasks.db`) and table are created automatically on first run — no manual setup needed.

## Endpoints

| Method | Path            | Description                | Success Code | Error Codes |
|--------|-----------------|-----------------------------|---------------|-------------|
| GET    | `/`             | API info                    | 200           | —           |
| GET    | `/health`       | Health check                 | 200           | —           |
| GET    | `/tasks`        | List all tasks               | 200           | —           |
| GET    | `/tasks/{id}`   | Get a single task by id      | 200           | 404         |
| POST   | `/tasks`        | Create a new task            | 201           | 400, 422    |
| PUT    | `/tasks/{id}`   | Replace an existing task     | 200           | 400, 404    |
| DELETE | `/tasks/{id}`   | Delete a task                | 204           | 404         |

## Example Request

```
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

![Swagger UI showing all endpoints](swagger-screenshot.png)

## Database Viewer

Opened with DB Browser for SQLite to inspect and manually query the data:

![DB Browser showing the tasks table](db-browser-screenshot.png)

Example query run manually:
```sql
SELECT * FROM tasks WHERE done = 1;
```

## Notes

Earlier versions of this API stored tasks in memory (a Python list), meaning all data was lost on restart. This version replaces that with a real SQLite database — the API's endpoints, request/response shapes, and status codes are unchanged; only the storage layer is different. This is the core lesson of this stage: APIs describe *what* an application does, databases describe *where* it stores its data.
```

**To finish:**
1. Save your DB Browser screenshot as `db-browser-screenshot.png` in your `task-api` folder
2. Replace the README's SQL example if you want to show the exact one you ran
3. Commit:
```bash
git add README.md db-browser-screenshot.png
git commit -m "Stage 5: database documentation"
git push
```