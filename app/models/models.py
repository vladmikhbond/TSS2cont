from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from datetime import datetime

class Base(DeclarativeBase):
    pass

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

class ProblemPostSchema(BaseModel):
    title: str
    attr: str
    lang: str
    cond: str
    view: str
    hint: str
    code: str
    author: str

    class Config:
        # orm_mode = True
        from_attributes=True

class ProblemSchema(ProblemPostSchema):
    id: str

    class Config:
        # orm_mode = True
        from_attributes=True
        

class CheckSchema(BaseModel):
    id: str
    solving: str

class ProofSchema(BaseModel):
    source: str
    lang: str

   
