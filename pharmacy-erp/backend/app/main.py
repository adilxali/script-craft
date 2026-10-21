from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import PharmacyERPException
from app.core.tenant_context import TenantContext, set_tenant_context, clear_tenant_context
from app.core.security import decode_jwt_token
from app.modules.identity.api import auth, organizations, branches, users, roles
from uuid import UUID

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Tenant Context Middleware
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = decode_jwt_token(token)
            branch_id_val = request.headers.get("X-Branch-ID") or payload.get("branch_id")
            ctx = TenantContext(
                organization_id=UUID(payload["org_id"]),
                branch_id=UUID(branch_id_val) if branch_id_val else None,
                user_id=UUID(payload["sub"]) if payload.get("sub") else None,
                is_platform_admin=payload.get("is_platform_admin", False)
            )
            set_tenant_context(ctx)
        except Exception:
            pass  # Route guards enforce valid authentication where required
            
    try:
        response = await call_next(request)
        return response
    finally:
        clear_tenant_context()

# Standard RFC 7807 Exception Handler
@app.exception_handler(PharmacyERPException)
async def pharmacy_erp_exception_handler(request: Request, exc: PharmacyERPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"https://errors.pharmacyerp.in/{exc.error_code.lower().replace('_', '-')}",
            "title": exc.error_code,
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": request.url.path,
            "invalid_params": exc.invalid_params
        }
    )

# Include Routers under API prefix /api/v1
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(organizations.router, prefix=settings.API_V1_STR)
app.include_router(branches.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(roles.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
def api_health_check():
    return {
        "status": "ONLINE",
        "api_version": "v1",
        "market": "IN"
    }
