```markdown
# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Tasks are stored in memory — data resets when the server restarts (no database yet, that's next week).

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

## Notes

Data is stored in-memory (a Python list) and is lost when the server restarts. This is intentional for this stage — persistence with a real database comes in the next assignment.
```


