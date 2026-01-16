import os
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db


# Use a separate SQLite DB just for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create all tables on the test DB
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the app's get_db dependency with the testing one
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_module(module):
    """
    Called once per test module.
    Ensure the DB is clean before running tests.
    """
    # Drop and recreate tables to start fresh
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ------------- TAG TESTS -------------


def test_create_tag():
    response = client.post("/tags", json={"name": "backend"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["name"] == "backend"


def test_create_duplicate_tag_fails():
    # First create
    client.post("/tags", json={"name": "frontend"})
    # Second with same name should fail
    response = client.post("/tags", json={"name": "frontend"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Tag name already exists"


def test_list_tags():
    response = client.get("/tags")
    assert response.status_code == 200
    data = response.json()
    # We created at least 2 tags in previous tests
    assert isinstance(data, list)
    assert len(data) >= 2
    names = [tag["name"] for tag in data]
    assert "backend" in names
    assert "frontend" in names


# ------------- TASK TESTS -------------


def test_create_task_with_tags():
    # Get tags to use their IDs
    tag_response = client.post("/tags", json={"name": "test-tag"})
    assert tag_response.status_code == 201
    tag_id = tag_response.json()["id"]

    tag_ids = [tag_id]


    payload = {
        "title": "Set up FastAPI backend",
        "description": "Wire Neon DB and health checks",
        "status": "pending",
        "due_date": None,
        "tag_ids": tag_ids,
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["title"] == payload["title"]
    assert data["status"] == "pending"
    assert len(data["tags"]) == 1
    assert data["tags"][0]["id"] == tag_ids[0]


def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert isinstance(data, list)
    # Check one item has expected fields
    task = data[0]
    assert "id" in task
    assert "title" in task
    assert "status" in task
    assert "tags" in task


def test_filter_tasks_by_status():
    # Create another task with a specific status
    payload = {
        "title": "Completed task example",
        "description": "Testing status filter",
        "status": "completed",
        "due_date": None,
        "tag_ids": [],
    }
    client.post("/tasks", json=payload)

    response = client.get("/tasks", params={"status": "completed"})
    assert response.status_code == 200
    data = response.json()
    assert all(task["status"] == "completed" for task in data)


def test_update_task_status():
    # Get any existing task
    list_response = client.get("/tasks")
    tasks = list_response.json()
    task_id = tasks[0]["id"]

    update_payload = {
        "status": "completed",
    }

    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == "completed"


def test_delete_task():
    # Create a new task to delete
    payload = {
        "title": "Task to delete",
        "description": "Will be removed in test",
        "status": "pending",
        "due_date": None,
        "tag_ids": [],
    }
    create_response = client.post("/tasks", json=payload)
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Confirm it's gone
    list_response = client.get("/tasks")
    tasks = list_response.json()
    ids = [t["id"] for t in tasks]
    assert task_id not in ids
