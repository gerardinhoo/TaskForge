from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import engine, Base, get_db
from . import models, schemas

# Models registered with SQLAlchemy before creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskForge API")

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


@app.get("/tasks", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    """
    Temporary basic GET endpoint.
    Returns all tasks from the database.
    """
    tasks = db.query(models.Task).order_by(models.Task.created_at.desc()).all()
    return tasks