from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import sqlite3

DB_FILE = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, like a dict
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    # Only seed example tasks if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Buy milk", False))
        conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Walk the dog", False))
        conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Finish backend homework", True))
    conn.commit()
    conn.close()

init_db()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

app = FastAPI()



@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [{**dict(row), "done": bool(row["done"])} for row in rows]

@app.get("/tasks/{task_id}", summary="Get a single task by id")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {**dict(row), "done": bool(row["done"])}

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(new_task: TaskCreate):
    title = new_task.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "title": title, "done": False}    

@app.put("/tasks/{task_id}", summary="Replace an existing task")
def update_task(task_id: int, updated: TaskUpdate):
    title = updated.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["done"] = updated.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

from fastapi import Response

@app.delete("/tasks/{task_id}", status_code=204, summary="delete a task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")