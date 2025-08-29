from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.orm import relationship

from db.session import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")