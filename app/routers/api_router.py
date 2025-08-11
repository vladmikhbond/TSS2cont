import datetime as dt
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request

from .. import data_alch as db
from ..models.models import Problem, ProofSchema, CheckSchema, ProblemSchema
from ..executors import js



import re

router = APIRouter()

# ============ Відкриті маршрути =============================

@router.post("/check")
async def post_check(schema: CheckSchema) -> str:
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
async def post_proof(schema: ProofSchema) -> str:
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

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .token_router import get_current_user


AuthType = Annotated[str, Depends(get_current_user)]

@router.get("/problems/lang")
async def get_problems_lang(lang: str, 
        # user: AuthType
    ) -> list[ProblemSchema]:
    """
    GET  /api/problems/lang/{lang}

    Повертає задачі для заданої мови програмування.
    """
    problems: list[Problem] = db.read_problems_lang(lang)
    # schemas: list[ProblemSchema] = [ProblemSchema.from_orm(p) for p in problems]
    return problems 


@router.get("/problems/{id}")
async def get_problems_id(id: str,
                        #   user: AuthType
                          ) -> ProblemSchema:
    """
    GET  /api/problems/{id}

    Повертає задачу з заданим id.
    """
    problem = db.read_problem(id) 
    if problem == None:
        raise HTTPException(status_code=404, detail=f"Error reading problem with id={id}")    
    problem_schema = ProblemSchema.model_validate(problem)
    return problem_schema


@router.post("/problems")
async def put_problems(problem_schema: ProblemSchema,
                    #    user: AuthType
                       ) :
    """
    POST /api/problems
    
    Перевіряє код і, якщо він годний, додає нову задачу в базу даних.
    """
    message = exec_helper(problem_schema.lang, problem_schema.code, timeout=2)
    if message.startswith("OK"):    

        problem = Problem(**problem_schema.model_dump())
 
        added_problem = db.add_problem(problem)
        if added_problem is None:
            raise HTTPException(status_code=400, detail="The problem is not added")
    return message


@router.put("/problems")
async def put_problems(problem_schema: ProblemSchema,
                    #    user: AuthType
                       ):
    """
    PUT /api/problems
    
    Перевіряє код і, якщо він годний, змінює задачу в базі даних.
    """
    message = exec_helper(problem_schema.lang, problem_schema.code, timeout=2)
    if message.startswith("OK"):          
        problem = Problem(**problem_schema.model_dump())
        changed_problem = db.edit_problem(problem)
        changed_problem.timestamp = dt.datetime.now() 
        if changed_problem is None:
            raise HTTPException(status_code=400, detail="The problem is not changed")
    return message



