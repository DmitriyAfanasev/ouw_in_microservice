from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.services.user_service.domain.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
)

P = ParamSpec("P")
T = TypeVar("T")


def handle_except_user_register(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except EmailAlreadyExists as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {e.email} already exists",
            ) from e
        except UsernameAlreadyExists as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username {e.username} already exists",
            ) from e
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists") from e
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return wrapper
