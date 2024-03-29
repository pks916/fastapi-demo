from .. import schemas, models, utils
from ..utils import hash_func
from ..db import get_db

from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[schemas.PostRespose])
def posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRespose)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostRespose)
def get_post(id:int, response: Response, db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post

@router.delete("/{id}")
def delete_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return {'data': post}

@router.put("/{id}", response_model=schemas.PostRespose)
def update_post(id:int, post: schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()