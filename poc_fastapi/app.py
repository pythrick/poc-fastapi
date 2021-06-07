import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

import config
from poc_fastapi.db.base import get_session
from poc_fastapi.exceptions import HealthCheckError, InternalServerError
from poc_fastapi.routers.auth import router as auth_router
from poc_fastapi.routers.post import router as post_router
from poc_fastapi.routers.user import router as user_router
from poc_fastapi.schemas.health_check import HealthCheckSchema
from poc_fastapi.services.health_check import health_check

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


@app.get(
    "/health-check", status_code=status.HTTP_200_OK, response_model=HealthCheckSchema
)
async def health_check_endpoint(session: AsyncSession = Depends(get_session)):
    try:
        await health_check(session)
    except Exception as e:
        raise HealthCheckError from e
    return HealthCheckSchema()


@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return await http_exception_handler(request, InternalServerError())


if __name__ == "__main__":
    uvicorn.run("poc_fastapi.app:app", reload=True)
