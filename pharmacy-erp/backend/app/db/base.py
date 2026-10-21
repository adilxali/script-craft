import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.clock_timestamp(),
        server_default=func.clock_timestamp(),
        nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.clock_timestamp(),
        server_default=func.clock_timestamp(),
        onupdate=func.clock_timestamp(),
        nullable=False
    )

class TenantScopedMixin:
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True
    )
