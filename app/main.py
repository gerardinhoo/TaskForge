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


@app.get("/tasks", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    """
    Temporary basic GET endpoint.
    Returns all tasks from the database.
    """
    tasks = db.query(models.Task).order_by(models.Task.created_at.desc()).all()
    return tasks