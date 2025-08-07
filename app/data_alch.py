import os

import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .models.models import Problem


# файл .db має знаходитися в кореневому каталозі пакета chat
DATA_BASE = os.path.join(os.path.dirname(__file__), "TSS2.db")

engine = create_engine(f"sqlite:///{DATA_BASE}", echo=True)


def read_all_problems() -> list[Problem]:
    with Session(engine) as session:
        probs = session.query(Problem).all()
    return probs

def read_problem(id: str) -> Problem:
    with Session(engine) as session:
        problem = session.query(Problem).filter(Problem.id == id).first()
    return problem

def read_problems_lang(lang: str) -> list[Problem]:
    with Session(engine) as session:
        problems = session.query(Problem).filter(Problem.lang == lang)
    return problems


# def add_item(message: str, sign: str):
#     datetime=dt.datetime.now().isoformat()
#     item = Item(message=message, sign=sign, datetime=datetime)

#     with Session(engine) as session:
#         session.add(item)        # додаємо об'єкт
#         session.commit()         # зберігаємо зміни
#         session .refresh(item)   # оновлюємо стан об'єкта

       
        