from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyQuery

from app.services.user_service.api.v1.auth import get_current_user
from app.services.user_service.api.v1.decorator_exception import (
    handle_except_user_register,
)
from app.services.user_service.domain.commands import CreateUserCommand
from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.domain.ports import (
    CreateUserUseCaseProtocol,
    UnitOfWorkProtocol,
    UserRepositoryProtocol,
)
from app.services.user_service.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
)

auth_scheme = APIKeyQuery(name="api_key")
ApiKey = Annotated[str, Depends(auth_scheme)]
CurrentUser = Annotated[UserEntity, Depends(get_current_user)]

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("/register", response_model=UserEntity, status_code=status.HTTP_201_CREATED)
# @inject - чтобы не инжектить каждую ручку, можно инжектить только на роутер указывая "route_class=DishkaRoute"
@handle_except_user_register
async def register_user(
    dto: UserCreateSchema,
    uc: FromDishka[CreateUserUseCaseProtocol],
) -> UserEntity:
    return await uc.execute(CreateUserCommand(**dto.model_dump()))


@router.patch("/update_me", response_model=UserEntity, status_code=status.HTTP_200_OK)
async def update_user_by_username(
    repository: FromDishka[UserRepositoryProtocol],
    dto: UserUpdateSchema,
    uow: FromDishka[UnitOfWorkProtocol],
) -> UserEntity:
    async with uow:
        return await repository.update_user(new_user_data=dto)


@router.get("/me", response_model=UserEntity, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: CurrentUser,
) -> UserEntity:
    return current_user


@router.post("/login", response_model=UserEntity, status_code=status.HTTP_200_OK)
async def login_user(
    repository: FromDishka[UserRepositoryProtocol],
    api_key: ApiKey,
) -> UserEntity:
    user = await repository.get_by_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return user
