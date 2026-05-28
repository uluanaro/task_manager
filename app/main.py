from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    description="API для управления задачами",
    version="0.1.0"
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
