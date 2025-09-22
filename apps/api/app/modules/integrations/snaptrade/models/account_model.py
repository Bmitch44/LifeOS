from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.modules.integrations.snaptrade.models.activity_model import SnaptradeActivity
    from app.modules.integrations.snaptrade.models.connection_model import SnaptradeConnection

class SnaptradeAccount(SQLModel, table=True):
    __tablename__ = "snaptrade_account"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    snaptrade_account_id: str = Field(nullable=True, unique=True, index=True)
    connection_id: int = Field(nullable=True, foreign_key="snaptrade_connection.id", ondelete="CASCADE")
    name: str = Field(nullable=True)
    number: str = Field(nullable=True)
    institution_name: str = Field(nullable=True)
    status: str = Field(nullable=True)
    type: str = Field(nullable=True)
    current_balance: float = Field(nullable=True)
    currency: str = Field(nullable=True)
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())

    connection: Optional["SnaptradeConnection"] = Relationship(
        back_populates="accounts",
        sa_relationship={"argument": "snaptrade_connection"}
    )

    activities: List["SnaptradeActivity"] = Relationship(
        back_populates="account",
        sa_relationship={"argument": "snaptrade_activity"},
        cascade_delete=True
    )