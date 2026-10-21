from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass(frozen=True)
class TenantContext:
    organization_id: UUID
    branch_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    is_platform_admin: bool = False

_current_tenant_ctx: ContextVar[Optional[TenantContext]] = ContextVar("current_tenant_ctx", default=None)

def set_tenant_context(ctx: TenantContext) -> None:
    _current_tenant_ctx.set(ctx)

def get_tenant_context() -> TenantContext:
    ctx = _current_tenant_ctx.get()
    if ctx is None:
        raise RuntimeError("CRITICAL: Operation attempted without an active TenantContext.")
    return ctx

def clear_tenant_context() -> None:
    _current_tenant_ctx.set(None)
