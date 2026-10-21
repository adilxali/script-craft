from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class OrganizationBase(BaseModel):
    legal_name: str = Field(..., max_length=255)
    trade_name: str = Field(..., max_length=255)
    gstin: Optional[str] = Field(None, max_length=15, pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
    pan: str = Field(..., max_length=10, pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
    drug_license_retail: Optional[str] = Field(None, max_length=100)
    drug_license_wholesale: Optional[str] = Field(None, max_length=100)
    currency: str = Field(default="INR", max_length=3)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    trade_name: Optional[str] = Field(None, max_length=255)
    drug_license_retail: Optional[str] = Field(None, max_length=100)
    drug_license_wholesale: Optional[str] = Field(None, max_length=100)

class OrganizationResponse(OrganizationBase):
    id: UUID
    status: str
    subscription_plan: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
