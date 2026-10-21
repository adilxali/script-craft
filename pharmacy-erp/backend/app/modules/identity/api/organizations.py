from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.identity.schemas.organization import OrganizationResponse, OrganizationUpdate
from app.modules.identity.repositories.organization_repository import OrganizationRepository
from app.core.dependencies import get_current_tenant_context, require_permission
from app.core.tenant_context import TenantContext
from app.core.permissions import PermissionCode

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.get(
    "/current",
    response_model=OrganizationResponse,
    dependencies=[Depends(require_permission(PermissionCode.ORGANIZATION_READ))]
)
def get_current_organization(
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = OrganizationRepository(db)
    org = repo.get_by_id(ctx.organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org

@router.put(
    "/current",
    response_model=OrganizationResponse,
    dependencies=[Depends(require_permission(PermissionCode.ORGANIZATION_UPDATE))]
)
def update_current_organization(
    req: OrganizationUpdate,
    ctx: TenantContext = Depends(get_current_tenant_context),
    db: Session = Depends(get_db)
):
    repo = OrganizationRepository(db)
    org = repo.get_by_id(ctx.organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    if req.trade_name is not None:
        org.trade_name = req.trade_name
    if req.drug_license_retail is not None:
        org.drug_license_retail = req.drug_license_retail
    if req.drug_license_wholesale is not None:
        org.drug_license_wholesale = req.drug_license_wholesale
        
    repo.update(org)
    db.commit()
    db.refresh(org)
    return org
