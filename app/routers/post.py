from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

"""Create Public Posts Section"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(posts: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO entries (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (entries.title, entries.content, entries.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Entry(title=entries.title, content=entries.content)
    # print(current_user.id)
    new_post = models.Post(user_id=current_user.id, **posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""SELECT * FROM entries""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM entries WHERE id = %s""", (str(id),))
    # entry = cursor.fetchone()
    single_post = db.query(models.Post).filter(models.Post.id==id).first()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The journal entry with the given id {id} doesn't exist")
    return single_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM entries WHERE id = %s RETURNING *""", (str(id)))
    # entry_to_delete = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
        return {"message": "post not found"}

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform the requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE entries SET title = %s, content = %s, WHERE id = %s RETURNING *""", (entry.title, entry.content, entry.published, (str(id))))
    # updated_entry = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Entry).filter(models.Entry.id==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
        return {"message": "Post not found"}

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform the requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()