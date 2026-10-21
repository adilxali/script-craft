from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.identity.models.user import User
from app.modules.identity.models.role import UserBranchAccess
from app.modules.identity.schemas.user import UserCreate, UserResponse
from app.modules.identity.services.identity_service import IdentityService
from app.core.dependencies import get_current_tenant_context, require_permission
from app.core.tenant_context import TenantContext
from app.core.permissions import PermissionCode
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "",
    response_model=List[UserResponse],
    dependencies=[Depends(require_permission(PermissionCode.USER_READ))]
)
def list_users(
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    users = service.user_repo.list_by_organization(ctx.organization_id)
    return [service._build_user_response(u) for u in users]

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.USER_CREATE))]
)
def create_user(
    req: UserCreate,
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    if service.user_repo.get_by_email(req.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{req.email}' already exists."
        )

    # Validate branch ownership within same organization
    branch = service.branch_repo.get_by_id(ctx.organization_id, req.branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified branch not found in organization."
        )

    # Validate role ownership within same organization
    role = service.role_repo.get_by_id(ctx.organization_id, req.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified role not found in organization."
        )

    user = User(
        organization_id=ctx.organization_id,
        email=req.email,
        phone=req.phone,
        password_hash=hash_password(req.password),
        full_name=req.full_name,
        registered_pharmacist_number=req.registered_pharmacist_number,
        pharmacist_reg_valid_until=req.pharmacist_reg_valid_until,
        is_active=True
    )
    service.user_repo.create(user)

    access = UserBranchAccess(
        user_id=user.id,
        organization_id=ctx.organization_id,
        branch_id=req.branch_id,
        role_id=req.role_id,
        is_default_branch=True
    )
    service.user_repo.add_branch_access(access)

    db.commit()
    return service._build_user_response(user)
