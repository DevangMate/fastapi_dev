from .. import models,schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select,update,func
from fastapi import APIRouter
from .. import oauth2
from typing import Optional,List

router = APIRouter(
    prefix="/posts",
    tags=['posts']
                   )


@router.get("/",response_model=List[schemas.Postout])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),Limit:int=10,skip:int=0,search:Optional[str]=""):

    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(Limit)
    # stmt=select(models.Post).where(models.Post.title.contains(search)).limit(Limit).offset(skip)
    # print(stmt)
    stmt2 = (
    select(models.Post, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id).where(models.Post.title.contains(search)).limit(Limit).offset(skip)
    )

    print(stmt2)
    
    posts=db.execute(stmt2).all()
    

    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.Postout)
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post=cursor.fetchone()
    stmt=(select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).where(models.Post.id==id)
    )
    post = db.execute(stmt).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id: {id} was not found"}
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that the id is located in
    # cursor.execute("""DELETE FROM posts   WHERE id=%s  RETURNING * """,(id,))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post=db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    if (post.owner_id!=current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    db.delete(post)
    # 4. Save the changes to Postgres
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#title should be string and content should be a string,category:


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title =%s ,content=%s,published=%s WHERE id=%s returning *""",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # 1. Find the post using our 2.0 shortcut
    post_to_update = db.get(models.Post, id)
    if post_to_update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesn't exist")
    if (post_to_update.owner_id!=current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    db.execute(
        update(models.Post)
        .where(models.Post.id == id)
        .values(**post.model_dump())
    )
    db.commit()
    db.refresh(post_to_update)
    return post_to_update


