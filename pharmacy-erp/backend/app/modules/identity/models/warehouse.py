from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, Numeric, ForeignKeyConstraint, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, TenantScopedMixin

class Warehouse(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "warehouses"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    branch_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    warehouse_code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "branch_id"],
            ["branches.organization_id", "branches.id"],
            ondelete="RESTRICT",
            name="fk_warehouse_branch"
        ),
        UniqueConstraint("organization_id", "branch_id", "warehouse_code", name="uq_warehouse_code"),
        UniqueConstraint("organization_id", "id", name="uq_warehouse_composite"),
    )

    branch = relationship("Branch", back_populates="warehouses")
    storage_locations = relationship("StorageLocation", back_populates="warehouse", cascade="all, delete-orphan")


class StorageLocation(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "storage_locations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    warehouse_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    zone: Mapped[str] = mapped_column(String(50), nullable=False)
    rack: Mapped[str] = mapped_column(String(50), nullable=False)
    shelf: Mapped[str] = mapped_column(String(50), nullable=False)
    bin: Mapped[str] = mapped_column(String(50), nullable=True)
    is_refrigerated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    temp_min_celsius: Mapped[float] = mapped_column(Numeric(4, 1), nullable=True)
    temp_max_celsius: Mapped[float] = mapped_column(Numeric(4, 1), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "warehouse_id"],
            ["warehouses.organization_id", "warehouses.id"],
            ondelete="RESTRICT",
            name="fk_storage_warehouse"
        ),
        UniqueConstraint("organization_id", "warehouse_id", "zone", "rack", "shelf", "bin", name="uq_storage_location"),
        UniqueConstraint("organization_id", "id", name="uq_storage_composite"),
    )

    warehouse = relationship("Warehouse", back_populates="storage_locations")
