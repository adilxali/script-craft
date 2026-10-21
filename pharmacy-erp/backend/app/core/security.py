import datetime
from typing import Any, Dict, Optional
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.core.config import settings

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(
    subject: str,
    org_id: str,
    branch_id: Optional[str] = None,
    is_platform_admin: bool = False,
    extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": subject,
        "org_id": org_id,
        "branch_id": branch_id,
        "is_platform_admin": is_platform_admin,
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)
        
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_jwt_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
