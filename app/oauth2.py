from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key #"ajkbirekn1F97FFBA63D7780nsngsbdscsm9A118A55yudfabsbksnagdujkfhsdvjabajksdgabasdkjasaajnlsa30E2C624C73E61BF22DB8F124F5"
ALGORITHM = settings.database_algorithm #"HS256"
TOKEN_EXPIRE_DAYS = 4

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    # c = json.dumps(expire, default=str)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authorize": "Bearer"})
    user_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_token.id).first()
    return user
