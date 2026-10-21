from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class PermissionResponse(BaseModel):
    id: UUID
    code: str
    description: str
    module: str

    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    permission_ids: List[UUID] = []

class RoleResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: Optional[str] = None
    is_system_role: bool
    created_at: datetime
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)
