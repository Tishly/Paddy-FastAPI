from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import engine, get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

"""Create User Section"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id: {id}")
    return user

@router.get("/all", response_model=schemas.UserOutput)
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id: {id}")
    return user