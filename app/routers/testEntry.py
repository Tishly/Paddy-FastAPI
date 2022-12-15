from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    tags=['Try Entries']
)

"""Create Journal Entries Section"""
@router.post("/{email}/entries", status_code=status.HTTP_201_CREATED, response_model=schemas.Entry)
def create_entries(email: str, entries: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO entries (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (entries.title, entries.content, entries.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Entry(title=entries.title, content=entries.content)
    # print(current_user.id)
    new_post = models.Entry(**entries.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{email}/entries", response_model=List[schemas.Entry])
def get_all_entries(email: str, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM entries""")
    # posts = cursor.fetchall()
    user_email = db.query(models.Tester).filter(models.Tester.email==email).first()
    if email == user_email:
        entries = db.query(models.Entry).filter(models.Entry.id==id).all()
    return entries


@router.get("/{email}/entries/{id}", response_model=schemas.Entry)
def get_one_entry(email: str, id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM entries WHERE id = %s""", (str(id),))
    # entry = cursor.fetchone()
    user_email = db.query(models.Tester).filter(models.Tester.email==email).first()
    if email == user_email:
        entry = db.query(models.Entry).filter(models.Entry.id==id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The journal entry with the given id {id} doesn't exist")

    # if entry.user_id != id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"You are not authorized to perform the requested action")

    return entry

@router.post("/tester", response_model=schemas.UserCollect)
def save_user(user: str = schemas.UserCollect, db: Session = Depends(get_db)):
    """"""
    user_email = db.query(models.Tester).filter(models.Tester.email==user.email).first()
    if not user_email:

        new_user = models.Tester(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return user_email

# @router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user