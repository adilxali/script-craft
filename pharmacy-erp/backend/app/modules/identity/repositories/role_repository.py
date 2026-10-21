from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.modules.identity.models.role import Role, Permission, RolePermission

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, org_id: UUID, role_id: UUID) -> Optional[Role]:
        return self.db.execute(
            select(Role)
            .options(joinedload(Role.role_permissions).joinedload(RolePermission.permission))
            .where(
                Role.organization_id == org_id,
                Role.id == role_id
            )
        ).unique().scalar_one_or_none()

    def get_by_name(self, org_id: UUID, name: str) -> Optional[Role]:
        return self.db.execute(
            select(Role)
            .where(
                Role.organization_id == org_id,
                Role.name == name
            )
        ).scalar_one_or_none()

    def list_by_organization(self, org_id: UUID) -> List[Role]:
        return list(
            self.db.execute(
                select(Role)
                .options(joinedload(Role.role_permissions).joinedload(RolePermission.permission))
                .where(Role.organization_id == org_id)
                .order_by(Role.name.asc())
            ).unique().scalars().all()
        )

    def list_permissions(self) -> List[Permission]:
        return list(self.db.execute(select(Permission).order_by(Permission.module, Permission.code)).scalars().all())

    def get_permissions_by_ids(self, permission_ids: List[UUID]) -> List[Permission]:
        return list(self.db.execute(select(Permission).where(Permission.id.in_(permission_ids))).scalars().all())

    def create(self, role: Role) -> Role:
        self.db.add(role)
        self.db.flush()
        return role

    def assign_permissions_to_role(self, role_id: UUID, permission_ids: List[UUID]) -> None:
        for pid in permission_ids:
            rp = RolePermission(role_id=role_id, permission_id=pid)
            self.db.add(rp)
        self.db.flush()
