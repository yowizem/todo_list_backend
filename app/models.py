from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base

class Post(Base):
    __tablename__ = "todo"

    todo_id = Column(Integer, primary_key=True, nullable=False)
    todo = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_done = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))