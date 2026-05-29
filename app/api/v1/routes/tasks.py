from fastapi import APIRouter, HTTPException, Depends
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.session import get_db
from app.models.task import Task
from sqlalchemy.orm import Session
# from datetime import datetime
from typing import List, Optional

router = APIRouter()


fake_db: list = []
counter: int = 0



@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        priority=task.priority
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # обновляем объект — получаем id и created_at из БД
    return new_task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.is_completed is not None:
        task.is_completed = task_update.is_completed
    if task_update.priority is not None:
        task.priority = task_update.priority

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(task)
    db.commit()

@router.get("/", response_model=List[TaskResponse])
def get_tasks(is_completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if is_completed is not None:
        query = query.filter(Task.is_completed == is_completed)
    return query.all()
