from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

from app.services.user_service.domain.commands import CreateUserCommand
from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.domain.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.services.user_service.domain.ports import (
    CreateUserUseCaseProtocol,
    UnitOfWorkProtocol,
    UserRepositoryProtocol,
)
from app.services.user_service.schemas import UserCreateSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("/register", response_model=UserEntity, status_code=status.HTTP_201_CREATED)
# @inject - чтобы не инжектить каждую ручку, можно инжектить только на роутер указывая "route_class=DishkaRoute"
async def register_user(
    dto: UserCreateSchema,
    uc: FromDishka[CreateUserUseCaseProtocol],
) -> UserEntity:
    try:
        return await uc.execute(CreateUserCommand(**dto.model_dump()))
    except (EmailAlreadyExists, UsernameAlreadyExists) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unique constraint violation") from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.patch("/update_me", response_model=UserEntity, status_code=status.HTTP_200_OK)
async def update_user_by_username(
    repository: FromDishka[UserRepositoryProtocol],
    dto: UserUpdateSchema,
    uow: FromDishka[UnitOfWorkProtocol],
) -> UserEntity:
    async with uow:
        return await repository.update_user(new_user_data=dto)


@router.get("/me", response_model=UserEntity, status_code=status.HTTP_200_OK)
async def get_user_by_username(
    repository: FromDishka[UserRepositoryProtocol],
    username: str = Query(
        "Ваш никнейм",
        title="Username",
        example="bigboss",
        deprecated=True,
        alias="логин",
        description=""" Длиннное описание """,
    ),
) -> UserEntity:
    return await repository.get_by_username(username)
