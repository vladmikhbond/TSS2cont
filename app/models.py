# from pydantic import BaseModel

# class Item(BaseModel):
#     id: int
#     message: str = ""
#     sign: str
#     datetime: str 

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Item(Base):
   __tablename__ = "items"
   id: Mapped[int] = mapped_column(primary_key=True)
   message: Mapped[str] = mapped_column()
   sign: Mapped[str] = mapped_column(String(30))
   datetime: Mapped[str] = mapped_column(String(50))

class Problem(Base):
    __tablename__ = "problems"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    attr: Mapped[str] = mapped_column(String(255))
    lang: Mapped[str] = mapped_column(String(5))
    cond: Mapped[str] = mapped_column(String)
    view: Mapped[str] = mapped_column(String)
    hint: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String(10))  
    timestamp: Mapped[str] = mapped_column(DateTime)