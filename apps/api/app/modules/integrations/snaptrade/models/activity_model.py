from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.modules.integrations.snaptrade.models.account_model import SnaptradeAccount

class SnaptradeActivity(SQLModel, table=True):
    __tablename__ = "snaptrade_activity"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    account_id: int = Field(nullable=True, foreign_key="snaptrade_account.id", ondelete="CASCADE")
    activity_id: str = Field(nullable=True)
    symbol_id: str = Field(nullable=True)
    option_symbol_id: str = Field(nullable=True)
    type: str = Field(nullable=True)
    option_type: str = Field(nullable=True)
    price: float = Field(nullable=True)
    units: float = Field(nullable=True)
    amount: float = Field(nullable=True)
    description: str = Field(nullable=True)
    trade_date: datetime = Field(nullable=True)
    settlement_date: datetime = Field(nullable=True)
    currency: str = Field(nullable=True)
    fees: float = Field(nullable=True)
    fx_rate: float = Field(nullable=True)
    institution: str = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})

    account: Optional["SnaptradeAccount"] = Relationship(
        back_populates="activities",
        sa_relationship={"argument": "snaptrade_account"}
    )