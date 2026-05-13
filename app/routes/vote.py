from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.schema import Vote
from app.utils.oauth2 import get_current_user
from app.models.model import Likes

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def do_vote(vote: Vote ,db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    vote_query = db.query(Likes).filter(Likes.post_id == vote.post_id, Likes.users_id == user.id)
    vote_found = vote_query.first()
    if (vote.dir):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Current user {user} has already voted to post")
        new_vote = Likes(post_id=vote.post_id, users_id=user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "VOTE ADDED NOW"}
    
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post is not voted yet")

        vote_query.delete(synchronize_session=False)

        db.commit()

        return{"message": status.HTTP_204_NO_CONTENT, "detail":"Post deleted success"}



    return  

