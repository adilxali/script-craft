import pytest
from uuid import uuid4
from app.core.tenant_context import TenantContext, set_tenant_context, clear_tenant_context

@pytest.fixture
def mock_tenant():
    org_id = uuid4()
    branch_id = uuid4()
    user_id = uuid4()
    ctx = TenantContext(
        organization_id=org_id,
        branch_id=branch_id,
        user_id=user_id,
        is_platform_admin=False
    )
    set_tenant_context(ctx)
    yield ctx
    clear_tenant_context()
