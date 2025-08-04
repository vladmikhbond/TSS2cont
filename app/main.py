from fastapi import FastAPI
from .routers import probs_router, token_router

app = FastAPI()

app.include_router(token_router.router, prefix="", tags=["token"])
app.include_router(probs_router.router, prefix="", tags=["problem"])

