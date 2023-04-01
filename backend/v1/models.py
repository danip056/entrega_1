from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, BOOLEAN
from sqlalchemy.sql import func
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, Mapped
from typing import List


Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER(), primary_key=True)
    user = Column(String(120), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(300))
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER(), primary_key=True)
    user_id = Column(INTEGER(), ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")
    original_file_name = Column(String(300))
    original_file_ext = Column(String(10))
    original_stored_file_name = Column(String(300))
    target_file_ext = Column(String(10))
    target_stored_file_name = Column(String(300))
    uploaded_at = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp())
    converted_at = Column(
        TIMESTAMP(),
        nullable=True,
        default=None,
    )
    status = Column(
        Enum("uploaded", "processed", name='status_types'),
        default="uploaded",
    )
