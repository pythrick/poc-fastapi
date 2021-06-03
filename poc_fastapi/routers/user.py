from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from poc_fastapi.db.base import get_session
from poc_fastapi.exceptions import UserAlreadyExistsError
from poc_fastapi.models.user import User
from poc_fastapi.schemas.auth import TokenSchema
from poc_fastapi.schemas.user import UserInSchema, UserSchema
from poc_fastapi.services import user as user_service
from poc_fastapi.services.auth import create_access_token
from poc_fastapi.services.user import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserInSchema, session: AsyncSession = Depends(get_session)
) -> TokenSchema:
    try:
        user_db = await user_service.create_user(session, user)
        await session.commit()
    except IntegrityError as e:
        raise UserAlreadyExistsError from e
    access_token = await create_access_token(user_db)
    return TokenSchema(**{"access_token": access_token, "token_type": "bearer"})


@router.get("/me", response_model=UserSchema)
async def profile_me_endpoint(
    current_user: User = Depends(get_current_active_user),
) -> UserSchema:
    return UserSchema.from_orm(current_user)
