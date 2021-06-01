from poc_fastapi.schemas.user import UserSchema


def test_user_schema(user):
    user_schema = UserSchema.from_orm(user)
    assert isinstance(user_schema, UserSchema)
