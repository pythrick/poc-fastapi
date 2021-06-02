import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import config
from poc_fastapi.db.base import init_models
from poc_fastapi.exceptions import InternalServerError
from poc_fastapi.routers.auth import router as auth_router
from poc_fastapi.routers.post import router as post_router
from poc_fastapi.routers.user import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return await http_exception_handler(request, InternalServerError())


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("poc_fastapi.app:app", reload=True)
