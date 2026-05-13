
from app.models.model import User
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import status, Depends
from fastapi import HTTPException
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from app.schemas.schema import TokenData, Token
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt  = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        if not id:
            # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            raise credentials_exception
        token_data = TokenData(id=id)
        return token_data
    except PyJWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code =status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    

    return user 