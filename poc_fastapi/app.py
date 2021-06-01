import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from poc_fastapi.db.base import init_models
from poc_fastapi.routers.post import router as post_router
from poc_fastapi.routers.user import router as user_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("poc_fastapi.app:app", reload=True)
