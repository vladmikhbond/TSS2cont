import os
from .models import Item, Problem
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# файл .db має знаходитися в кореневому каталозі пакета chat
DATA_BASE = os.path.join(os.path.dirname(__file__), "TSS2.db")

engine = create_engine(f"sqlite:///{DATA_BASE}", echo=True)


def read_all_probs() -> list[Problem]:
    with Session(engine) as session:
        probs = session.query(Problem).all()
    return probs


# def add_item(message: str, sign: str):
#     datetime=dt.datetime.now().isoformat()
#     item = Item(message=message, sign=sign, datetime=datetime)

#     with Session(engine) as session:
#         session.add(item)        # додаємо об'єкт
#         session.commit()         # зберігаємо зміни
#         session .refresh(item)   # оновлюємо стан об'єкта

       
        