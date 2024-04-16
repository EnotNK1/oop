import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from typing import List


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)

    word: Mapped[List["Word"]] = relationship()

class Word(Base):
    __tablename__ = "word"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    word: Mapped[str]
    translate: Mapped[str]
    user_email: Mapped[str] = mapped_column(ForeignKey("users.email", ondelete="CASCADE"))