from typing import Dict
from fastapi import APIRouter, Depends
from sqlmodel import Session
from Database.ORM_Models.auth_models import *
from Database.ORM_Models.token_models import Token
from Auth.functions import authenticate_user, get_user_detail, create_jwt, hash_password, get_session
from Http_Exceptions.exceptions import wrong_authentication, user_not_found, user_already_exist

auth_router = APIRouter()

@auth_router.post("/auth/login")
def user_login(login_data: UserLoginRequest, session: Session = Depends(get_session)) -> Token:
    if (authenticate_user(login_data,session)):
        user_detail = get_user_detail(login_data.aadhaar_number,login_data.user_type,session)
        if user_detail is None:
            raise user_not_found
        access_token = create_jwt({"sub": user_detail.full_name, "pk": login_data.aadhaar_number, "user_type": login_data.user_type})
        return Token(access_token=access_token,token_type="bearer")
    else:
        raise wrong_authentication
    
@auth_router.post("/auth/signup")
def user_signup(signup_data: UserSignupRequest, session: Session = Depends(get_session)) -> Dict:
    user_detail = get_user_detail(signup_data.aadhaar_number,signup_data.user_type,session)
    if user_detail is not None:
        raise user_already_exist
    signup_data_dict = signup_data.model_dump()
    signup_data_dict.update({"hashed_password": hash_password(signup_data.password)})
    new_user = UserInDB(**signup_data_dict)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Successfull SignUp"}