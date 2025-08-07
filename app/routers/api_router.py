from typing import Annotated, Dict
from fastapi import APIRouter, Depends, Request

from .. import data_alch as db
from ..models.models import Problem, PostProof, PostCheck, ProblemSchema
from ..executors import js


import re

router = APIRouter()

# ============ Відкриті маршрути =============================

@router.post("/check")
async def post_check(schema: PostCheck) -> str:
    """
    POST /api/check

    Знаходить задачу, замінює авторське вирішення користувацьким,
    викликає post_proof()
    """
    problem = db.read_problem(schema.id)
    regex = regex_helper(problem.lang);
    if regex == None:
       return "Wrong Language" 
    newCode = re.sub(regex, schema.solving, problem.code, count=1, flags=re.DOTALL)
    return exec_helper(problem.lang, newCode, timeout=2)
     

@router.post("/proof")
async def post_proof(schema: PostProof) -> str:
    """
    POST /api/proof

    Виконує програму, повертає повідомлення про результат.
    Повідомлення про позитивний результат починається з OK
    """
    return exec_helper(schema.lang, schema.source, timeout=2)
    
         
def regex_helper(lang:str):
    if lang == 'js':
        return r"//BEGIN.*//END"
    return None


def exec_helper(lang:str, source: str, timeout: float):
    if lang == 'js':
        return js.exec(source, timeout=timeout)
    return "Error: Unknown language"

# ============ Закриті маршрути =============================

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/problems/lang")
async def get_problems_lang(lang: str, token: Annotated[str, Depends(oauth2_scheme)]) -> list[ProblemSchema]:
    """
    GET  /api/problems/lang/{lang}

    Повертає задачі для заданої мови програмування.
    """
    problems: list[Problem] = db.read_problems_lang(lang)
    # schemas: list[ProblemSchema] = [ProblemSchema.from_orm(p) for p in problems]
    return problems 
    



