from sqlmodel import Session
from typing import Generator
from Database.Engine import engine
from dotenv import load_dotenv
from passlib.context import CryptContext
from Database.ORM_Models.auth_models import UserLoginRequest, UserInDB, UserType
from typing import cast
import os
import jwt


SECRET_KEY="7165de02e0e87f1f89a7ab20598d39fc476383d23c529017fa55e107a7157480"
ALGORITHM="HS256"

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def hash_password(original_password: str) -> str:
    return pwdContext.hash(original_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwdContext.verify(plain_password,hashed_password)

def authenticate_user(data: UserLoginRequest, session: Session) -> bool:
    if data.user_type == UserType.USER:
        db_data = session.get(UserInDB, data.aadhaar_number)
        if db_data is None:
            return False
        if (verify_password(data.password,db_data.hashed_password)):
            return True
        else:
            return False
    else:
        return False
    
def get_user_detail(aadhaar_number: str, user_type: str, session: Session) -> UserInDB | None:
    if user_type==UserType.USER:
        result = session.get(UserInDB,aadhaar_number)
        if result is not None:
            return result
        return None
    else:
        return None
    
def create_jwt(data: dict):
    copied_data = data.copy()
    encoded_jwt = jwt.encode(copied_data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt