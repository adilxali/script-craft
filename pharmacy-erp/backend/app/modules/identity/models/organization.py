import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trade_name: Mapped[str] = mapped_column(String(255), nullable=False)
    gstin: Mapped[str] = mapped_column(String(15), unique=True, nullable=True)
    pan: Mapped[str] = mapped_column(String(10), nullable=False)
    drug_license_retail: Mapped[str] = mapped_column(String(100), nullable=True)
    drug_license_wholesale: Mapped[str] = mapped_column(String(100), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE",
        nullable=False
    )
    subscription_plan: Mapped[str] = mapped_column(
        String(50),
        default="PROFESSIONAL",
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'ONBOARDING', 'ARCHIVED')",
            name="chk_organization_status"
        ),
    )

    # Relationships
    branches = relationship("Branch", back_populates="organization", cascade="all, delete-orphan")
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="organization", cascade="all, delete-orphan")
