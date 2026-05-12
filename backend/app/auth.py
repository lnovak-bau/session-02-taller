import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Secret key for signing JWTs – set the SECRET_KEY environment variable in production
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pre-computed bcrypt hash of "admin123" – avoids re-hashing on every startup.
# Regenerate with: python -c "from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('admin123'))"
_ADMIN_HASHED_PASSWORD = (
    "$2b$12$/5yvThg5fQIpN3zm/YNxNe3B08Q2hJA9Oh54vdErWzI.nm3NrUhei"
)

# Fake user database
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": _ADMIN_HASHED_PASSWORD,
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = FAKE_USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire_seconds = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises JWTError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
