from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from app.modules.integrations.snaptrade.models import SnaptradeConnection
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate, SnaptradeConnectionUpdate, PaginatedSnaptradeConnections


class SnaptradeConnectionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, clerk_user_id: str, page: int, size: int) -> PaginatedSnaptradeConnections:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(SnaptradeConnection).where(SnaptradeConnection.clerk_user_id == clerk_user_id)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            connections_query = select(SnaptradeConnection).where(SnaptradeConnection.clerk_user_id == clerk_user_id).offset(offset).limit(size)
            connections_result = await self.session.execute(connections_query)
            connections = connections_result.scalars().all()
            return PaginatedSnaptradeConnections(items=connections, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: SnaptradeConnectionCreate) -> SnaptradeConnection:
        try:
            connection = SnaptradeConnection(
                clerk_user_id=payload.clerk_user_id,
                connection_id=payload.connection_id,
                brokerage_name=payload.brokerage_name,
                user_secret=payload.user_secret
            )
            self.session.add(connection)
            await self.session.commit()
            await self.session.refresh(connection)
            return connection
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> SnaptradeConnection:
        try:
            connection = await self.session.get(SnaptradeConnection, id)
            if not connection:
                raise HTTPException(status_code=404, detail="Connection not found")
            return connection
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_clerk_user_id(self, clerk_user_id: str) -> SnaptradeConnection:
        try:
            connection = await self.session.execute(select(SnaptradeConnection).where(SnaptradeConnection.clerk_user_id == clerk_user_id))
            return connection.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SnaptradeConnectionUpdate) -> SnaptradeConnection:
        try:
            connection = await self.session.get(SnaptradeConnection, id)
            if not connection:
                raise HTTPException(status_code=404, detail="Connection not found")
            connection.clerk_user_id = payload.clerk_user_id
            connection.connection_id = payload.connection_id
            connection.brokerage_name = payload.brokerage_name
            connection.user_secret = payload.user_secret
            await self.session.commit()
            await self.session.refresh(connection)
            return connection
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            connection = await self.session.get(SnaptradeConnection, id)
            if not connection:
                raise HTTPException(status_code=404, detail="Connection not found")
            await self.session.delete(connection)
            await self.session.commit()
            return {"message": "Connection deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e