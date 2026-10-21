from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.modules.identity.models.user import User
from app.modules.identity.models.role import UserBranchAccess, Role, Permission, RolePermission

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, org_id: UUID, user_id: UUID) -> Optional[User]:
        return self.db.execute(
            select(User)
            .options(
                joinedload(User.branch_accesses).joinedload(UserBranchAccess.branch),
                joinedload(User.branch_accesses).joinedload(UserBranchAccess.role)
            )
            .where(
                User.organization_id == org_id,
                User.id == user_id
            )
        ).unique().scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.execute(
            select(User)
            .options(
                joinedload(User.branch_accesses).joinedload(UserBranchAccess.branch),
                joinedload(User.branch_accesses).joinedload(UserBranchAccess.role)
            )
            .where(User.email == email)
        ).unique().scalar_one_or_none()

    def list_by_organization(self, org_id: UUID) -> List[User]:
        return list(
            self.db.execute(
                select(User)
                .options(
                    joinedload(User.branch_accesses).joinedload(UserBranchAccess.branch),
                    joinedload(User.branch_accesses).joinedload(UserBranchAccess.role)
                )
                .where(User.organization_id == org_id)
                .order_by(User.full_name.asc())
            ).unique().scalars().all()
        )

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def add_branch_access(self, access: UserBranchAccess) -> UserBranchAccess:
        self.db.add(access)
        self.db.flush()
        return access

    def get_user_permissions_in_branch(self, user_id: UUID, branch_id: UUID) -> List[str]:
        # Query permissions assigned to the role held by user in the specific branch
        stmt = (
            select(Permission.code)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(Role, RolePermission.role_id == Role.id)
            .join(UserBranchAccess, UserBranchAccess.role_id == Role.id)
            .where(
                UserBranchAccess.user_id == user_id,
                UserBranchAccess.branch_id == branch_id
            )
        )
        return list(self.db.execute(stmt).scalars().all())
