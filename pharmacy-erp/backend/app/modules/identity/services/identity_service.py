from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.identity.models.organization import Organization
from app.modules.identity.models.branch import Branch
from app.modules.identity.models.user import User
from app.modules.identity.models.role import Role, Permission, UserBranchAccess
from app.modules.identity.schemas.organization import OrganizationCreate
from app.modules.identity.schemas.branch import BranchCreate
from app.modules.identity.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse, BranchAccessDTO
from app.modules.identity.schemas.role import RoleCreate
from app.modules.identity.repositories.organization_repository import OrganizationRepository
from app.modules.identity.repositories.branch_repository import BranchRepository
from app.modules.identity.repositories.user_repository import UserRepository
from app.modules.identity.repositories.role_repository import RoleRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import PharmacyERPException, TenantIsolationException
from app.core.permissions import PermissionCode
from fastapi import status

class IdentityService:
    def __init__(self, db: Session):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.branch_repo = BranchRepository(db)
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    def seed_system_permissions(self) -> None:
        """Seeds standard permissions if not already existing."""
        for code in PermissionCode:
            module = code.value.split(".")[0]
            existing = self.db.query(Permission).filter_by(code=code.value).first()
            if not existing:
                p = Permission(
                    code=code.value,
                    description=f"Permission for {code.value}",
                    module=module
                )
                self.db.add(p)
        self.db.flush()

    def provision_organization(
        self,
        org_data: OrganizationCreate,
        admin_name: str,
        admin_email: str,
        admin_phone: str,
        admin_password: str,
        initial_branch: BranchCreate
    ) -> Tuple[Organization, Branch, User]:
        """Complete vertical slice: Onboard new pharmacy organization with owner and default branch."""
        # 1. Check GSTIN uniqueness
        if org_data.gstin and self.org_repo.get_by_gstin(org_data.gstin):
            raise PharmacyERPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization with GSTIN {org_data.gstin} already exists.",
                error_code="GSTIN_ALREADY_EXISTS"
            )

        # 2. Check Admin email uniqueness
        if self.user_repo.get_by_email(admin_email):
            raise PharmacyERPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {admin_email} already exists.",
                error_code="USER_EMAIL_EXISTS"
            )

        # 3. Create Organization
        org = Organization(
            legal_name=org_data.legal_name,
            trade_name=org_data.trade_name,
            gstin=org_data.gstin,
            pan=org_data.pan,
            drug_license_retail=org_data.drug_license_retail,
            drug_license_wholesale=org_data.drug_license_wholesale,
            currency=org_data.currency
        )
        self.org_repo.create(org)

        # 4. Create Initial Branch
        branch = Branch(
            organization_id=org.id,
            branch_code=initial_branch.branch_code,
            name=initial_branch.name,
            branch_type=initial_branch.branch_type,
            state_code=initial_branch.state_code,
            gstin=initial_branch.gstin or org.gstin,
            drug_license_number=initial_branch.drug_license_number,
            pharmacist_in_charge_name=initial_branch.pharmacist_in_charge_name,
            pharmacist_reg_number=initial_branch.pharmacist_reg_number,
            address_line1=initial_branch.address_line1,
            address_line2=initial_branch.address_line2,
            city=initial_branch.city,
            pincode=initial_branch.pincode,
            phone=initial_branch.phone,
            email=initial_branch.email or admin_email
        )
        self.branch_repo.create(branch)

        # 5. Seed default Owner role with all permissions
        self.seed_system_permissions()
        all_perms = self.role_repo.list_permissions()
        owner_role = Role(
            organization_id=org.id,
            name="Pharmacy Owner",
            description="Full access to all pharmacy operations, finances and settings",
            is_system_role=True
        )
        self.role_repo.create(owner_role)
        self.role_repo.assign_permissions_to_role(owner_role.id, [p.id for p in all_perms])

        # 6. Create Admin User
        user = User(
            organization_id=org.id,
            email=admin_email,
            phone=admin_phone,
            password_hash=hash_password(admin_password),
            full_name=admin_name,
            is_active=True
        )
        self.user_repo.create(user)

        # 7. Grant Admin User Access to the Initial Branch
        access = UserBranchAccess(
            user_id=user.id,
            organization_id=org.id,
            branch_id=branch.id,
            role_id=owner_role.id,
            is_default_branch=True
        )
        self.user_repo.add_branch_access(access)

        self.db.commit()
        return org, branch, user

    def authenticate_user(self, login_data: UserLogin) -> TokenResponse:
        user = self.user_repo.get_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise PharmacyERPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password credentials.",
                error_code="INVALID_CREDENTIALS"
            )

        if not user.is_active:
            raise PharmacyERPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated. Contact organization owner.",
                error_code="USER_DEACTIVATED"
            )

        # Determine active branch
        accessible_branches = user.branch_accesses
        if not accessible_branches and not user.is_platform_admin:
            raise PharmacyERPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no branch assignments.",
                error_code="NO_BRANCH_ACCESS"
            )

        active_branch_id = login_data.branch_id
        if not active_branch_id and accessible_branches:
            # Pick default branch or first available
            default_acc = next((b for b in accessible_branches if b.is_default_branch), accessible_branches[0])
            active_branch_id = default_acc.branch_id

        # Verify user has access to active branch
        if active_branch_id and not any(b.branch_id == active_branch_id for b in accessible_branches):
            raise TenantIsolationException("Access to specified branch is not granted.")

        # Permissions in active branch
        permissions = []
        if active_branch_id:
            permissions = self.user_repo.get_user_permissions_in_branch(user.id, active_branch_id)

        # Issue JWT
        token = create_access_token(
            subject=str(user.id),
            org_id=str(user.organization_id),
            branch_id=str(active_branch_id) if active_branch_id else None,
            is_platform_admin=user.is_platform_admin,
            extra_claims={"perms": permissions}
        )

        user_response = self._build_user_response(user)
        return TokenResponse(
            access_token=token,
            expires_in=60 * 8 * 60, # 8 hours in seconds
            user=user_response,
            active_branch_id=active_branch_id,
            permissions=permissions
        )

    def switch_branch(self, user_id: UUID, org_id: UUID, target_branch_id: UUID) -> TokenResponse:
        user = self.user_repo.get_by_id(org_id, user_id)
        if not user:
            raise PharmacyERPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Verify access to target branch
        if not any(b.branch_id == target_branch_id for b in user.branch_accesses):
            raise TenantIsolationException("Access to requested branch is not granted.")

        permissions = self.user_repo.get_user_permissions_in_branch(user.id, target_branch_id)
        token = create_access_token(
            subject=str(user.id),
            org_id=str(user.organization_id),
            branch_id=str(target_branch_id),
            is_platform_admin=user.is_platform_admin,
            extra_claims={"perms": permissions}
        )

        return TokenResponse(
            access_token=token,
            expires_in=60 * 8 * 60,
            user=self._build_user_response(user),
            active_branch_id=target_branch_id,
            permissions=permissions
        )

    def _build_user_response(self, user: User) -> UserResponse:
        branch_dtos = [
            BranchAccessDTO(
                branch_id=acc.branch_id,
                branch_code=acc.branch.branch_code if acc.branch else "",
                branch_name=acc.branch.name if acc.branch else "",
                role_name=acc.role.name if acc.role else "",
                is_default=acc.is_default_branch
            )
            for acc in user.branch_accesses
        ]
        return UserResponse(
            id=user.id,
            organization_id=user.organization_id,
            email=user.email,
            phone=user.phone,
            full_name=user.full_name,
            registered_pharmacist_number=user.registered_pharmacist_number,
            pharmacist_reg_valid_until=user.pharmacist_reg_valid_until,
            is_active=user.is_active,
            is_platform_admin=user.is_platform_admin,
            created_at=user.created_at,
            branches=branch_dtos
        )
