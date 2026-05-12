from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    authenticate_user,
    create_access_token,
    decode_token,
)

app = FastAPI(title="JWT Auth API", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    token: str


class UserOut(BaseModel):
    username: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return UserOut(username=username)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/token", response_model=TokenResponse, summary="Obtain a JWT access token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with **username** and **password**.

    - Default credentials: `admin` / `admin123`
    - The token expires in **300 seconds**.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/token/refresh", response_model=TokenResponse, summary="Refresh a JWT access token")
def refresh_token(body: RefreshRequest):
    """
    Provide a **valid** (non-expired) token and receive a new one with a
    fresh 300-second expiration window.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(body.token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_token = create_access_token(data={"sub": username})
    return TokenResponse(
        access_token=new_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.get("/me", response_model=UserOut, summary="Get current authenticated user")
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    """Protected endpoint – requires a valid Bearer token."""
    return current_user
