from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    branch_id: Optional[UUID] = None

class UserCreate(BaseModel):
    email: EmailStr
    phone: str = Field(..., max_length=20)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., max_length=255)
    registered_pharmacist_number: Optional[str] = None
    pharmacist_reg_valid_until: Optional[date] = None
    role_id: UUID
    branch_id: UUID

class BranchAccessDTO(BaseModel):
    branch_id: UUID
    branch_code: str
    branch_name: str
    role_name: str
    is_default: bool

class UserResponse(BaseModel):
    id: UUID
    organization_id: UUID
    email: str
    phone: str
    full_name: str
    registered_pharmacist_number: Optional[str] = None
    pharmacist_reg_valid_until: Optional[date] = None
    is_active: bool
    is_platform_admin: bool
    created_at: datetime
    branches: List[BranchAccessDTO] = []

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    active_branch_id: Optional[UUID] = None
    permissions: List[str] = []

class SwitchBranchRequest(BaseModel):
    branch_id: UUID
