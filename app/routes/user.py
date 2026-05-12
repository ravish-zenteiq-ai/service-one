from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.schema import createUser
from app.models.model import User
from app.utils.pass_hash import  create_hash

router = APIRouter(
    prefix="/user",
    tags=["User"]
)
@router.get("/users")
async def get_users( db: Session = Depends(get_db)):
    users =db.query(User).all()
    return users
@router.post("/")
async def create_user(create: createUser,db: Session = Depends(get_db)):
    hashed = create_hash(create.password)   
    create.password = hashed

    # new_user = User(name = create.name, email = create.email, password = create.password, job = create.job)
    new_user = User(**create.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    get_one = db.query(User).filter(User.id == id).first()
    if not get_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is not post create 1st post")
    return get_one

