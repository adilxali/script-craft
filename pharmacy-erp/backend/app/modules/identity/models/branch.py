from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, CheckConstraint, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, TenantScopedMixin

class Branch(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "branches"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    branch_code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_type: Mapped[str] = mapped_column(String(50), nullable=False)
    state_code: Mapped[str] = mapped_column(String(2), nullable=False)
    gstin: Mapped[str] = mapped_column(String(15), nullable=True)
    drug_license_number: Mapped[str] = mapped_column(String(100), nullable=False)
    pharmacist_in_charge_name: Mapped[str] = mapped_column(String(255), nullable=True)
    pharmacist_reg_number: Mapped[str] = mapped_column(String(100), nullable=True)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str] = mapped_column(String(6), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "branch_type IN ('RETAIL', 'WHOLESALE_DEPOT', 'HOSPITAL_INTERNAL', 'CENTRAL_WAREHOUSE')",
            name="chk_branch_type"
        ),
        CheckConstraint(
            "pincode ~ '^[1-9][0-9]{5}$'",
            name="chk_branch_pincode"
        ),
        UniqueConstraint("organization_id", "branch_code", name="uq_branch_org_code"),
        UniqueConstraint("organization_id", "id", name="uq_branch_composite"),
    )

    organization = relationship("Organization", back_populates="branches")
    warehouses = relationship("Warehouse", back_populates="branch", cascade="all, delete-orphan")
    user_accesses = relationship("UserBranchAccess", back_populates="branch", cascade="all, delete-orphan")
