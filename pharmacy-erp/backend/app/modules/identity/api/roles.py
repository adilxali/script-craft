from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.identity.models.role import Role
from app.modules.identity.schemas.role import RoleCreate, RoleResponse, PermissionResponse
from app.modules.identity.repositories.role_repository import RoleRepository
from app.core.dependencies import get_current_tenant_context, require_permission
from app.core.tenant_context import TenantContext
from app.core.permissions import PermissionCode

router = APIRouter(prefix="/roles", tags=["Roles & Permissions"])

@router.get(
    "",
    response_model=List[RoleResponse],
    dependencies=[Depends(require_permission(PermissionCode.ROLE_READ))]
)
def list_roles(
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = RoleRepository(db)
    roles = repo.list_by_organization(ctx.organization_id)
    response = []
    for r in roles:
        perms = [rp.permission for rp in r.role_permissions if rp.permission]
        response.append(
            RoleResponse(
                id=r.id,
                organization_id=r.organization_id,
                name=r.name,
                description=r.description,
                is_system_role=r.is_system_role,
                created_at=r.created_at,
                permissions=[PermissionResponse.model_validate(p) for p in perms]
            )
        )
    return response

@router.get(
    "/permissions",
    response_model=List[PermissionResponse],
    dependencies=[Depends(require_permission(PermissionCode.ROLE_READ))]
)
def list_permissions(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    return repo.list_permissions()

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.ORGANIZATION_UPDATE))]
)
def create_role(
    req: RoleCreate,
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = RoleRepository(db)
    if repo.get_by_name(ctx.organization_id, req.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role with name '{req.name}' already exists in organization."
        )

    role = Role(
        organization_id=ctx.organization_id,
        name=req.name,
        description=req.description,
        is_system_role=False
    )
    repo.create(role)

    if req.permission_ids:
        repo.assign_permissions_to_role(role.id, req.permission_ids)

    db.commit()
    db.refresh(role)
    perms = [rp.permission for rp in role.role_permissions if rp.permission]
    return RoleResponse(
        id=role.id,
        organization_id=role.organization_id,
        name=role.name,
        description=role.description,
        is_system_role=role.is_system_role,
        created_at=role.created_at,
        permissions=[PermissionResponse.model_validate(p) for p in perms]
    )
