# створення і налаштування об'єкта додатку app

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from .data_alch import do_test_db
from .routers import items_router


app = FastAPI()



app.include_router(items_router.router, prefix="", tags=["auth"])

do_test_db()