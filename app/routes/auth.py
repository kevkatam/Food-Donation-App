from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import get_user_by_username
from app.utils import get_password_hash, verify_password
import os


"""secret key and algorithm for JWT"""
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
"""environment variable for secret key, with default fallback"""

ALGORITHM = "HS256" # algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 300 # Token expiration time in mins

"""Initialize password context for hass=hing and verifying passwords"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""OAuth2PasswordBearer instance to get token from request"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    """
    authenticate the user by verifying the username and password
    returns the user if authentication is successful, otherwise returns false
    """
    user = await get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    """ function that creates a JWT access token with an expirarion time """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ function that gets the current user from the provided JWT token.
    Raises an HTTP 401 error if the token is invalid or the user does not exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
