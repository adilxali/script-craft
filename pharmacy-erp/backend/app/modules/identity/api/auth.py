from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.identity.schemas.user import UserLogin, TokenResponse, SwitchBranchRequest, UserResponse
from app.modules.identity.schemas.organization import OrganizationCreate
from app.modules.identity.schemas.branch import BranchCreate
from app.modules.identity.services.identity_service import IdentityService
from app.core.dependencies import get_current_user_token_payload, get_current_tenant_context
from app.core.tenant_context import TenantContext
from pydantic import BaseModel, EmailStr
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication & Identity"])

class OrganizationOnboardRequest(BaseModel):
    organization: OrganizationCreate
    admin_name: str
    admin_email: EmailStr
    admin_phone: str
    admin_password: str
    initial_branch: BranchCreate

@router.post("/onboard", status_code=status.HTTP_201_CREATED)
def onboard_organization(
    req: OrganizationOnboardRequest,
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    org, branch, admin_user = service.provision_organization(
        org_data=req.organization,
        admin_name=req.admin_name,
        admin_email=req.admin_email,
        admin_phone=req.admin_phone,
        admin_password=req.admin_password,
        initial_branch=req.initial_branch
    )
    # Auto-login newly created admin
    return service.authenticate_user(
        UserLogin(email=req.admin_email, password=req.admin_password, branch_id=branch.id)
    )

@router.post("/login", response_model=TokenResponse)
def login(
    req: UserLogin,
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    return service.authenticate_user(req)

@router.post("/switch-branch", response_model=TokenResponse)
def switch_branch(
    req: SwitchBranchRequest,
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    return service.switch_branch(
        user_id=ctx.user_id,
        org_id=ctx.organization_id,
        target_branch_id=req.branch_id
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    user = service.user_repo.get_by_id(ctx.organization_id, ctx.user_id)
    return service._build_user_response(user)
