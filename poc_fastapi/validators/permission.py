from typing import Set

from fastapi import Depends

from poc_fastapi.exceptions import OperationNotPermittedError
from poc_fastapi.models import User
from poc_fastapi.services.user import (
    get_current_active_user,
    list_user_perms,
    list_user_roles,
)


class PermissionValidator:
    def __init__(self, required_perms: Set[str], allowed_roles: Set[str]):
        """
        Validator to check if user have enough permission to proceed
        :param required_perms: user should have ALL required permission listed here
        :param allowed_roles: user should have AT LEAST ONE of roles listed here
        """

        self.required_perms = required_perms
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(get_current_active_user)) -> None:
        user_roles = await list_user_roles(user)
        if "admin" in user_roles:
            return
        user_perms = await list_user_perms(user)

        if self.allowed_roles and not self.allowed_roles & user_roles:
            raise OperationNotPermittedError

        if self.required_perms and not self.required_perms <= user_perms:
            raise OperationNotPermittedError
