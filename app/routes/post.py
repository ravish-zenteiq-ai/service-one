
from typing import Optional
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.model import Post
from app.schemas.schema import (
    createPost,
    returnPost
)
from app.utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)


@router.get("/")
async def get_posts(db: Session = Depends(get_db),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(f"limit is {limit} and skip is {skip} and we are searching is {search}" )
    get_post = db.query(Post).filter(Post.description.contains(search)).limit(limit).offset(skip).all()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is not post create 1st post")
    return get_post

@router.get("/my")
async def my_post(
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user),
    limit: int = 10
):  
    print(limit)
    get_post = db.query(Post).filter(Post.owner_id == user.id).all()
    if not get_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is not post create 1st post")
    return get_post


@router.post("/", response_model=returnPost)
async def create_post(create: createPost,db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # new_Post = Post(title = create.title, description= create.description, owner_id=user_id.id)
    new_Post = Post(owner_id=user_id.id ,**create.dict())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    return new_Post

@router.get("/{id}")
async def get_post(id: int,
    user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    one_Post = db.query(Post).filter(Post.id == id).first()
    if not one_Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is not post with id = {id}")
    if one_Post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this post")

    return one_Post

@router.put("/{id}")
async def update_post(
    update: createPost,
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    find_post= db.query(Post).filter(Post.id == id)
    
    if not find_post.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This post is not available anymore")
    
    if find_post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to UPDATE this post")

    
    updated_post = find_post.update({
        "title": update.title,
        "description": update.description
        }, synchronize_session=False
    )
    db.commit()
    # db.refresh(updated_post)
    return find_post.first()

@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    find = db.query(Post).filter(Post.id == id)
    if not find.first( ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This post is not available anymore")
    if find.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    find.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post has been delelted"}