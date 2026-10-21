from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.identity.models.branch import Branch
from app.modules.identity.schemas.branch import BranchCreate, BranchResponse
from app.modules.identity.repositories.branch_repository import BranchRepository
from app.core.dependencies import get_current_tenant_context, require_permission
from app.core.tenant_context import TenantContext
from app.core.permissions import PermissionCode

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get(
    "",
    response_model=List[BranchResponse],
    dependencies=[Depends(require_permission(PermissionCode.BRANCH_READ))]
)
def list_branches(
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = BranchRepository(db)
    return repo.list_by_organization(ctx.organization_id)

@router.post(
    "",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionCode.BRANCH_CREATE))]
)
def create_branch(
    req: BranchCreate,
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = BranchRepository(db)
    if repo.get_by_code(ctx.organization_id, req.branch_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Branch code '{req.branch_code}' already exists in your organization."
        )

    branch = Branch(
        organization_id=ctx.organization_id,
        branch_code=req.branch_code,
        name=req.name,
        branch_type=req.branch_type,
        state_code=req.state_code,
        gstin=req.gstin,
        drug_license_number=req.drug_license_number,
        pharmacist_in_charge_name=req.pharmacist_in_charge_name,
        pharmacist_reg_number=req.pharmacist_reg_number,
        address_line1=req.address_line1,
        address_line2=req.address_line2,
        city=req.city,
        pincode=req.pincode,
        phone=req.phone,
        email=req.email
    )
    repo.create(branch)
    db.commit()
    db.refresh(branch)
    return branch
