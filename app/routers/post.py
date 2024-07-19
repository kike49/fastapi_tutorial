from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


# Retrieve all posts
@router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    # Instead of using pure SQL queries, we connect through a ORM with SQLAlchemy and run the queries in Python. The SQL code is now commented on all the methods
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts_with_votes = [{"post": post.__dict__, "votes": votes} for post, votes in results]
    return posts_with_votes


# Retrieve one specific post
@router.get("/{id}", response_model=schemas.PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post_found = cursor.fetchone()
    post_found = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return post_found


# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserLogin = Depends(oauth2.get_current_user)): #This arguments are; new_post: the input from user based on the schema defined, db: the database connection by using the get_db function defined in database.py, current_user: the user needs to be logged in by passing the id to the path and comparing it with the one logged in.
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.published))
    # created_post = cursor.fetchall()
    # conn.commit()
    # To unpack the args of the Post model, we can do this: created_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published) but that requires manual entry of each colums of our table. Instead we will conver that model into a dict using the following syntax to unpack the arguments of the model Post into the table according to what the user inputs:
    created_post = models.Post(owner_id = current_user.id, **new_post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # for p in my_posts:
    #     if p['id'] == id:
    #         my_posts.remove(p)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_delete = post_query.first()
    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot delete this post because your don't owe it. Your user id is {current_user.id} and the post was created by the user id {post_to_delete.owner_id}")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot update this post because your don't owe it. Your user id is {current_user.id} and the post was created by the user id {post_to_update.owner_id}")
    # Update the fields of the post without the update method:
    # for key, value in updated_post.model_dump(exclude_unset=True).items():
    #     setattr(post_to_update, key, value)
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    # db.refresh(post_to_update)
    return post_query.first()
