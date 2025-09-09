from uuid import UUID

from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.infrastructure.db.models import ApiKey
from app.services.user_service.infrastructure.db.models import User as UserModel
from app.services.user_service.schemas import UserUpdateSchema


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_user(self, user: UserEntity) -> UserModel:
        model = UserModel.from_entity(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(UserModel).where(UserModel.email == email)
        user = (await self.session.execute(stmt)).scalar_one()
        return user.to_entity()

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

    async def create_api_key(self, user_id: UUID) -> str:
        api_key = ApiKey(user_id=user_id)
        self.session.add(api_key)
        stmt = update(UserModel).where(UserModel.id == user_id).values(api_key=ApiKey())
        await self.session.execute(stmt)
        return str(api_key.id)

    async def get_by_api_key(self, api_key: str) -> UserEntity:
        stmt = (
            select(UserModel)
            .join(UserModel.api_key)
            .where(ApiKey.id == api_key, ApiKey.is_active == True)
            .options(joinedload(UserModel.api_key))
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one()
        return user.to_entity()

    async def check_unique_email_and_username(self, username: str, email: str) -> tuple[str | None, str | None]:
        """
        Проверяет, существуют ли пользователь с таким email или username.
        Возвращает кортеж (email, username), если такие уже есть в БД.
        """
        stmt = select(UserModel.email, UserModel.username).where(
            or_(UserModel.email == email, UserModel.username == username)
        )
        result = await self.session.execute(stmt)
        rows = result.fetchall()

        # Ищем совпадения
        found_email = None
        found_username = None

        for row in rows:
            if row.email == email:
                found_email = email
            if row.username == username:
                found_username = username

        return found_email, found_username
