from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base, get_db
from . import models, schemas

# Models registered with SQLAlchemy before creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskForge API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.get("/tags", response_model=list[schemas.Tag])
def list_tags(db: Session = Depends(get_db)):
    """
    List all tags.
    """
    tags = db.query(models.Tag).order_by(models.Tag.name.asc()).all()
    return tags


@app.post("/tags", response_model=schemas.Tag, status_code=201)
def create_tag(payload: schemas.TagCreate, db: Session = Depends(get_db)):
    """
    Create a new tag.
    Tag names must be unique.
    """
    existing = db.query(models.Tag).filter(models.Tag.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag name already exists")

    tag = models.Tag(name=payload.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@app.post("/tasks", response_model=schemas.Task, status_code=201)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task with optional tags.
    """
    # Base task fields
    task = models.Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        due_date=payload.due_date,
    )

    # Attach tags if tag_ids provided
    if payload.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(payload.tag_ids)).all()
        if len(tags) != len(payload.tag_ids):
            raise HTTPException(status_code=400, detail="One or more tags not found")
        task.tags = tags

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing task. Only fields provided will be updated.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update simple fields if provided
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status
    if payload.due_date is not None:
        task.due_date = payload.due_date

    # Update tags if tag_ids provided
    if payload.tag_ids is not None:
        if len(payload.tag_ids) == 0:
            # Clear tags if empty list
            task.tags = []
        else:
            tags = db.query(models.Tag).filter(models.Tag.id.in_(payload.tag_ids)).all()
            if len(tags) != len(payload.tag_ids):
                raise HTTPException(status_code=400, detail="One or more tags not found")
            task.tags = tags

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing task.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return

@app.get("/tasks", response_model=List[schemas.Task])
def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    tag_id: Optional[int] = Query(None, description="Filter by tag id"),
    db: Session = Depends(get_db),
):
    """
    List tasks with optional filtering by status and tag.
    """
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)

    if tag_id:
        query = query.join(models.Task.tags).filter(models.Tag.id == tag_id)

    tasks = query.order_by(models.Task.created_at.desc()).all()
    return tasks