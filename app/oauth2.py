import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas,models
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings 
from datetime import datetime, timedelta, timezone
#things that weneed to provide
#SECRET KEY
#algorithm
#expiration date 

# to get a string like this run:
# openssl rand -hex 32
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM

def create_access_token(data:dict):

    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        # Safely convert it to a string for Pydantic V2
        id: str = str(user_id)
        token_data=schemas.TokenData(id=id)
    except InvalidTokenError:
        # This catches expired, tampered, or malformed tokens
        raise credentials_exception
        
    return token_data 

def get_current_user(token:str =Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data= verify_access_token(token,credentials_exception)
    id=token_data.id
    user=db.get(models.User, id)
    return user

