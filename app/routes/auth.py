from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schema import loginUser, Token
from app.db.session import get_db
from app.utils.pass_hash import verify_hash
from app.models.model import User
from app.utils.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
# async def login(login: loginUser,
async def login(login: OAuth2PasswordRequestForm = Depends(),
db: Session = Depends(get_db)
):
    verifyEmail = db.query(User).filter(User.email == login.username).first()
    if not verifyEmail:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential")
    verifypass = verify_hash(login.password, verifyEmail.password)
    if not verifypass:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential")
    access_token = create_access_token(data = {"user_id": verifyEmail.id})
    

    return{"access_token": access_token, "token_type": "bearer"}