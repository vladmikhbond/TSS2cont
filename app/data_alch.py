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
    try:
        with Session(engine) as session:
            problem = session.query(Problem).filter(Problem.id == id).first()
        return problem
    except Exception as e:
        print(f"Error reading problem with id={id}: {e}")
        return None


def read_problems_lang(lang: str) -> list[Problem]:
    with Session(engine) as session:
        problems = session.query(Problem).filter(Problem.lang == lang)
    return problems


def add_problem(problem: Problem):
    with Session(engine) as session:
        session.add(problem)        # додаємо об'єкт
        session.commit()         # зберігаємо зміни
        

       
        