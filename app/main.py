from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from .db import engine

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