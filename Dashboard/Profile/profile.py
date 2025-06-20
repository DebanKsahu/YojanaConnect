from fastapi import APIRouter,Depends
from Auth.functions import oauth2_scheme, get_session, SECRET_KEY, ALGORITHM
from sqlmodel import Session, select
from Database.ORM_Models.auth_models import UserInDB
from Database.ORM_Models.profile_models import ProfileExpose, ProfileEdit
from Http_Exceptions.exceptions import user_not_found, wrong_authentication
import jwt

profile_router  = APIRouter()


@profile_router.get("/profile",response_model=ProfileExpose)
def get_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    return user_detail

@profile_router.patch("/profile/edit")
def edit_profile(new_data: ProfileEdit, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    new_data_dict = new_data.model_dump(exclude_unset=True)
    user_detail.sqlmodel_update(new_data_dict)
    session.add(user_detail)
    session.commit()
    session.refresh(user_detail)
    return {"message": "Update Successfully"}