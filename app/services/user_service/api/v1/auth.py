from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyQuery
from sqlalchemy.exc import IntegrityError

from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.domain.ports import UserRepositoryProtocol

auth_scheme = APIKeyQuery(name="api_key")


@inject
async def get_current_user(
    repository: FromDishka[UserRepositoryProtocol],
    api_key: str = Security(auth_scheme),
) -> UserEntity:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
        )
    try:
        user = await repository.get_by_api_key(api_key)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is invalid",
        )
    return user
