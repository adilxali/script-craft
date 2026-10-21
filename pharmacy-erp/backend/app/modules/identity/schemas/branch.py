from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class BranchBase(BaseModel):
    branch_code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=255)
    branch_type: str = Field(..., pattern=r"^(RETAIL|WHOLESALE_DEPOT|HOSPITAL_INTERNAL|CENTRAL_WAREHOUSE)$")
    state_code: str = Field(..., max_length=2, pattern=r"^[0-9]{2}$")
    gstin: Optional[str] = Field(None, max_length=15)
    drug_license_number: str = Field(..., max_length=100)
    pharmacist_in_charge_name: Optional[str] = Field(None, max_length=255)
    pharmacist_reg_number: Optional[str] = Field(None, max_length=100)
    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=100)
    pincode: str = Field(..., pattern=r"^[1-9][0-9]{5}$")
    phone: str = Field(..., max_length=20)
    email: Optional[str] = Field(None, max_length=255)

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    pharmacist_in_charge_name: Optional[str] = Field(None, max_length=255)
    pharmacist_reg_number: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class BranchResponse(BranchBase):
    id: UUID
    organization_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
