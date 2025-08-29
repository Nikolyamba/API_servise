import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.get_db import get_db
from models.answer_model import Answer
from models.question_model import Question

a_router = APIRouter() #answer as a

class CreateAnswer(BaseModel):
    question_id: int
    user_id: uuid.UUID
    text: str

class GetAnswer(BaseModel):
    id: int
    question_id: int
    user_id: uuid.UUID
    text: str
    created_at: datetime

    class Config:
        orm_mode = True

@a_router.post("/questions/{id}/answers", response_model = GetAnswer)
async def create_answer(data: CreateAnswer, id: int, db: Session = Depends(get_db)):
    try:
        question = db.query(Question).filter(Question.id == id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Такого вопроса нет!")
        new_answer = Answer(question_id = id,
                            user_id = data.user_id,
                            text = data.text)
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)
        return new_answer
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")

@a_router.get("/answers/{id}", response_model = GetAnswer)
async def get_answer(id: int, db: Session = Depends(get_db)):
    try:
        answer = db.query(Answer).filter(Answer.id == id).first()
        if not answer:
            raise HTTPException(status_code=404, detail="Такого ответа не существует!")
        return answer
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")

@a_router.delete("/answers/{id}")
async def delete_answer(id: int, db: Session = Depends(get_db)) -> dict:
    try:
        answer = db.query(Answer).filter(Answer.id == id).first()
        if not answer:
            raise HTTPException(status_code=404, detail="Такого ответа не существует!")
        answer_id = answer.id
        db.delete(answer)
        db.commit()
        return {"success": True, "message": f"Ответ с id: {answer_id} успешно удалён"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")
