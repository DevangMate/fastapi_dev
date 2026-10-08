from .. import models,schemas,database,models,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select,update

from fastapi import APIRouter

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.get(models.Post,vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id {vote.post_id} does not exist")
    stmt = select(models.Vote).where(
    models.Vote.post_id == vote.post_id, 
    models.Vote.user_id == current_user.id
    )

# fetch the first result or None
    found_vote = db.scalars(stmt).first()
    print(found_vote)
    
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already voted on post{vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote doesnot exist")
        db.delete(found_vote)
        db.commit()
        return {"message":"deleted vote succesfully"}