from fastapi import FastAPI

app = FastAPI(title="TaskForge API")

@app.get("/health")

def health():
    return {"status": "ok"}