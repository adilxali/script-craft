from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.identity.models.branch import Branch

class BranchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, org_id: UUID, branch_id: UUID) -> Optional[Branch]:
        return self.db.execute(
            select(Branch).where(
                Branch.organization_id == org_id,
                Branch.id == branch_id
            )
        ).scalar_one_or_none()

    def get_by_code(self, org_id: UUID, branch_code: str) -> Optional[Branch]:
        return self.db.execute(
            select(Branch).where(
                Branch.organization_id == org_id,
                Branch.branch_code == branch_code
            )
        ).scalar_one_or_none()

    def list_by_organization(self, org_id: UUID, is_active: Optional[bool] = None) -> List[Branch]:
        query = select(Branch).where(Branch.organization_id == org_id)
        if is_active is not None:
            query = query.where(Branch.is_active == is_active)
        return list(self.db.execute(query.order_by(Branch.branch_code.asc())).scalars().all())

    def create(self, branch: Branch) -> Branch:
        self.db.add(branch)
        self.db.flush()
        return branch
