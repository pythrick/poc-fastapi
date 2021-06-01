import pytest

from poc_fastapi.exceptions import InvalidPassword


def test_user_model_set_password(user, faker):
    user.hashed_password = None
    plain_password = faker.pystr()
    user.set_password(plain_password)
    assert user.hashed_password is not None
    assert user.hashed_password != plain_password
    assert user.verify_password(plain_password)


def test_user_model_verify_invalid_password(user, faker):
    user.set_password("pa$$w0rD")
    with pytest.raises(InvalidPassword):
        user.verify_password("password")
