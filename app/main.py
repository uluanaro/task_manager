from fastapi import FastAPI
from app.api.v1.routes import tasks
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Manager API",
    description="API для управления задачами",
    version="0.1.0"
)

app.include_router(
    tasks.router,
    prefix="/api/v1/tasks",
    tags=["tasks"]
)

@app.get("/")
def root():
    return {"message": "Task Manager API работает!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def version_of_task_manager():
    return {"version": "0.1.0",
            "author": "Uluana Roshina"
            }
