from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.infrastructure.db.models import User as UserModel
from app.services.user_service.schemas import UserUpdateSchema


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: UserEntity) -> UserModel:
        model = UserModel.from_entity(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(UserModel).where(UserModel.email == email)
        user = (await self.session.execute(stmt)).scalar_one()
        return user.to_entity()

    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        user = await self.session.get(UserModel, user_id)
        return user.to_entity() if user else None

    async def get_by_username(self, username: str) -> UserEntity:
        stmt = select(UserModel).where(UserModel.username == username)
        user = (await self.session.execute(stmt)).scalar_one()
        return user.to_entity()

    async def update_user(self, new_user_data: UserUpdateSchema) -> UserEntity:
        stmt = (
            update(UserModel)
            .where(UserModel.id == new_user_data.id)
            .values(**new_user_data.model_dump(exclude_none=True))
        )
        await self.session.execute(stmt)
        stmt_get_user = select(UserModel).where(UserModel.id == new_user_data.id)
        user = (await self.session.execute(stmt_get_user)).scalar_one()
        return user.to_entity()
