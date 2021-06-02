from fastapi import APIRouter, Depends, status

from poc_fastapi.db.base import get_session
from poc_fastapi.schemas.auth import RequestTokenSchema, TokenSchema
from poc_fastapi.services.auth import authenticate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def get_access_token(body: RequestTokenSchema, session=Depends(get_session)):
    access_token = await authenticate(session, **body.dict())
    return TokenSchema(**{"access_token": access_token, "token_type": "bearer"})
