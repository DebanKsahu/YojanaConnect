from sqlmodel import SQLModel
from Database.ORM_Models.auth_models import UserType

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str | None = None
    user_type: UserType