import asyncio

import uvicorn
from fastapi import FastAPI

from poc_fastapi.db.base import init_models
from poc_fastapi.routers.post import router as post_router
from poc_fastapi.routers.user import router as user_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("poc_fastapi.app:app", reload=True)
