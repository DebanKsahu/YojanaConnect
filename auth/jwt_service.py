from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from auth import *
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

async def verifyToken(token : Annotated[str, Depends(oauth2_scheme)]):
    try:
        print(token)
        ##verification logic here: jwt.decode(token , SECRET_KEY , algorithm=[ALGORITHM])
    except Exception as e:
        raise http_exceptions.Exceptions['unauthorized_error']


        