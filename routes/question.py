from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.get_db import get_db
from models.question_model import Question

q_router = APIRouter() #question as q

class CreateQuestion(BaseModel):
    text: str

class GetQuestion(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True

@q_router.post("/questions", response_model=GetQuestion)
async def create_question(data: CreateQuestion, db: Session = Depends(get_db)):
    """Создание вопроса"""
    try:
        new_question = Question(text = data.text,
                                created_at = data.datetime)
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        return new_question
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")
@q_router.get("/questions", response_model=List[GetQuestion])
async def get_all_questions(db: Session = Depends(get_db)):
    """Функция получения всех вопросов"""
    try:
        all_questions = db.query(Question).order_by(Question.created_at).all()
        return all_questions
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")

@q_router.delete("/questions/{id}")
async def delete_question(id: int, db: Session = Depends(get_db)) -> dict:
    """Удаление вопроса по его id"""
    try:
        question = db.query(Question).filter(Question.id == id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Такой вопрос не найден!")
        question_id = question.id
        db.delete(question)
        db.commit()
        return {"success": True, "message": f"Вопрос с id {question_id} успешно удалён!"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")

