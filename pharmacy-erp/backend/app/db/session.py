from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings
from app.core.tenant_context import get_tenant_context

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        # Set PostgreSQL session variable for Row-Level Security if tenant context exists
        try:
            ctx = get_tenant_context()
            if ctx and ctx.organization_id:
                db.execute(text(f"SET LOCAL app.current_organization_id = '{ctx.organization_id}'"))
        except RuntimeError:
            pass # Unauthenticated or pre-tenant health check
            
        yield db
    finally:
        db.close()
