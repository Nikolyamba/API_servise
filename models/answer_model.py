import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, UUID
from sqlalchemy.orm import relationship

from db.session import Base

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4) #В ТЗ user_id указан как строка (например, uuid). Так как база — PostgreSQL, я использовал нативный тип UUID, чтобы было оптимальнее
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("Question", back_populates="answers")