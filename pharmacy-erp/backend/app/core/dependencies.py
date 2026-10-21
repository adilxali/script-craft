from typing import Callable, List
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_jwt_token
from app.core.tenant_context import TenantContext, get_tenant_context, set_tenant_context
from app.core.permissions import PermissionCode
from uuid import UUID

security = HTTPBearer()

def get_current_user_token_payload(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_tenant_context(
    payload: dict = Depends(get_current_user_token_payload)
) -> TenantContext:
    try:
        return get_tenant_context()
    except RuntimeError:
        # Fallback if middleware didn't catch (e.g. in test client)
        ctx = TenantContext(
            organization_id=UUID(payload["org_id"]),
            branch_id=UUID(payload["branch_id"]) if payload.get("branch_id") else None,
            user_id=UUID(payload["sub"]) if payload.get("sub") else None,
            is_platform_admin=payload.get("is_platform_admin", False)
        )
        set_tenant_context(ctx)
        return ctx

def require_permission(permission: PermissionCode) -> Callable:
    def permission_checker(payload: dict = Depends(get_current_user_token_payload)) -> None:
        if payload.get("is_platform_admin"):
            return # Platform admins bypass tenant-level role checks where applicable
        
        user_perms: List[str] = payload.get("perms", [])
        if permission.value not in user_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: Missing required permission '{permission.value}'."
            )
    return permission_checker
