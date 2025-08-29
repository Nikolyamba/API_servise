from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

a_router = APIRouter() #answer as a

class CreateAnswer(BaseModel):
    question_id: int
    user_id: str
    text: str
    created_at: datetime

class GetAnswer(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime