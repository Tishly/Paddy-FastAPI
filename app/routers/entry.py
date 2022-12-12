from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/entries",
    tags=['Entries']
)

"""Create Journal Entries Section"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Entry)
def create_entries(entries: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO entries (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (entries.title, entries.content, entries.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Entry(title=entries.title, content=entries.content)
    # print(current_user.id)
    new_post = models.Entry(user_id=current_user.id, **entries.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.Entry])
def get_all_entries(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM entries""")
    # posts = cursor.fetchall()
    entries = db.query(models.Entry).filter(models.Entry.user_id == current_user.id).all()
    return entries


@router.get("/{id}", response_model=schemas.Entry)
def get_one_entry(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM entries WHERE id = %s""", (str(id),))
    # entry = cursor.fetchone()
    entry = db.query(models.Entry).filter(models.Entry.id==id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The journal entry with the given id {id} doesn't exist")

    if entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform the requested action")

    return entry


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM entries WHERE id = %s RETURNING *""", (str(id)))
    # entry_to_delete = cursor.fetchone()
    # conn.commit()
    entry_query = db.query(models.Entry).filter(models.Entry.id==id)
    entry = entry_query.first()

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
        return {"message": "post not found"}

    if entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform the requested action")

    entry_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Entry)
def update_post(id: int, updated_entry: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE entries SET title = %s, content = %s, WHERE id = %s RETURNING *""", (entry.title, entry.content, entry.published, (str(id))))
    # updated_entry = cursor.fetchone()
    # conn.commit()
    entry_query = db.query(models.Entry).filter(models.Entry.id==id)
    entry = entry_query.first()

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Entry with id {id} was not found")
        return {"message": "Entry not found"}

    if entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform the requested action")

    entry_query.update(updated_entry.dict(), synchronize_session=False)
    db.commit()
    return entry_query.first()