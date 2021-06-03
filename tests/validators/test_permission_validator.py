from contextlib import nullcontext as dont_raise
from unittest.mock import AsyncMock

import pytest

from poc_fastapi.exceptions import OperationNotPermittedError
from poc_fastapi.validators.permission import PermissionValidator


@pytest.mark.parametrize(
    ("user_perms", "user_roles", "required_perms", "allowed_roles", "raise_exc"),
    (
        (
            {
                "create-user",
            },
            {"writer"},
            {"create-user"},
            {"writer"},
            dont_raise(),
        ),
        (
            {"create-user", "read-user", "update-user"},
            {"writer", "reader", "reviewer"},
            {"create-user", "update-user"},
            {"writer", "publisher"},
            dont_raise(),
        ),
        (
            {},
            {"admin"},
            {"create-user"},
            {"writer"},
            dont_raise(),
        ),
        (
            {
                "read-user",
            },
            {"reader"},
            {"create-user"},
            {"reader"},
            pytest.raises(OperationNotPermittedError),
        ),
        (
            {
                "read-user",
            },
            {"reader"},
            {"read-user"},
            {"writer"},
            pytest.raises(OperationNotPermittedError),
        ),
    ),
    ids=[
        "User has the right permission and role",
        "User has more permissions than need and at least one of the allowed roles",
        "User has admin role",
        "User has not enough permission",
        "User has not enough roles",
    ],
)
@pytest.mark.asyncio
async def test_permission_validator(
    mock_get_current_active_user,
    mocker,
    user_perms,
    user_roles,
    required_perms,
    allowed_roles,
    raise_exc,
):
    mocker.patch(
        "poc_fastapi.validators.permission.list_user_perms",
        side_effect=AsyncMock(return_value=user_perms),
    )
    mocker.patch(
        "poc_fastapi.validators.permission.list_user_roles",
        side_effect=AsyncMock(return_value=user_roles),
    )

    validate = PermissionValidator(required_perms, allowed_roles)
    with raise_exc:
        await validate()
