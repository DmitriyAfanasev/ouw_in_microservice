from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.services.user_service.domain.commands import CreateUserCommand
from app.services.user_service.domain.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.services.user_service.domain.use_cases import CreateUserUseCase
from app.services.user_service.schemas import UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    dto: UserCreateSchema,
    uc: FromDishka[CreateUserUseCase],
) -> UserResponseSchema:
    try:
        user = await uc.execute(CreateUserCommand(**dto.model_dump()))
    except (EmailAlreadyExists, UsernameAlreadyExists) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Unique constraint violation"
        ) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return UserResponseSchema.model_validate(user)
