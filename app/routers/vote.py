from sys import prefix
from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):
    post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) #This query checks on the DB if the post has already been voted by the user logged in
    found_vote = vote_query.first()
    if (vote.dir == 1): #This represents the user wants to vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user {current_user.id} has already vote on the post {vote.post_id} so it cannot be done again")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"Successfully voted on the post {vote.post_id} by the user {current_user.id}"}
    else: #This represents the user wants to unlike/unvote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist, you haven't vote on this post so you cannot perform an unlike")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote/like successfully deleted"}