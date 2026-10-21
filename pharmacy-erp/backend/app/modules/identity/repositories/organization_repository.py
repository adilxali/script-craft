from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.identity.models.organization import Organization

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, org_id: UUID) -> Optional[Organization]:
        return self.db.execute(
            select(Organization).where(Organization.id == org_id)
        ).scalar_one_or_none()

    def get_by_gstin(self, gstin: str) -> Optional[Organization]:
        return self.db.execute(
            select(Organization).where(Organization.gstin == gstin)
        ).scalar_one_or_none()

    def create(self, organization: Organization) -> Organization:
        self.db.add(organization)
        self.db.flush()
        return organization

    def update(self, organization: Organization) -> Organization:
        self.db.flush()
        return organization
