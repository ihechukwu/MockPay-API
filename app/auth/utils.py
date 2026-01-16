from email.policy import HTTP
from pwdlib import PasswordHash
import jwt
from datetime import timedelta, datetime
from app.core.config import settings
from jwt.exceptions import PyJWTError
from fastapi import HTTPException, status
import uuid
from itsdangerous import URLSafeTimedSerializer


password_hash = PasswordHash.recommended()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTE

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def generate_password_hash(password: str):

    return password_hash.hash(password)


def verify_password_hash(plain_passowrd: str, hashed_password: str) -> bool:

    return password_hash.verify(plain_passowrd, hashed_password)


def create_access_token(
    data: dict, expires_delta: timedelta = None, refresh: bool = False
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4), "refresh": refresh})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        return payload

    except PyJWTError:
        raise credentials_exception


token_serializer = URLSafeTimedSerializer(
    secret_key=SECRET_KEY, salt="email-verification"
)


def create_url_safe_token(data: dict):
    token = token_serializer.dumps(data)
    return token


def decode_url_safe_token(token: str):
    try:
        token_data = token_serializer.loads(token)
        return token_data

    except Exception:
        raise credentials_exception
