from fastapi import APIRouter,Depends
from Auth.functions import oauth2_scheme, get_session
from sqlmodel import Session, select
from Database.ORM_Models.auth_models import UserInDB, UserAddressInDB
from Database.ORM_Models.profile_models import ProfileExpose, ProfileEdit
from Database.ORM_Models.criteria_models import CriteriaInDB, CriteriaEdit, CriteriaExpose
from Http_Exceptions.exceptions import user_not_found, wrong_authentication, criteria_already_exist, criteria_not_found, missiing_value_exception
from config import settings
import jwt

profile_router  = APIRouter()


@profile_router.get("/profile",response_model=ProfileExpose)
def get_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    user_detail_dict = user_detail.model_dump()
    user_detail_dict["user_address"]=user_detail.address_detail
    print(user_detail.address_detail)
    return user_detail_dict

@profile_router.get("/profile/criteria")
def get_criteria(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    result: list[CriteriaExpose] = []
    for criteria in user_detail.user_criteria:
        result.append(CriteriaExpose(**criteria.model_dump()))
    return result

@profile_router.patch("/profile/edit")
def edit_profile(new_data: ProfileEdit, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    new_data_dict = new_data.model_dump(exclude_unset=True)
    if "user_address" in new_data_dict:
        new_address_detail_dict = new_data_dict.pop("user_address")
        user_address = session.get(UserAddressInDB,logged_user_pk)
        if user_address is None:
            new_address_detail_dict["aadhaar_number"]=logged_user_pk
            new_user_address = UserAddressInDB(**new_address_detail_dict)
            session.add(new_user_address)
        else:
            user_address.sqlmodel_update(new_address_detail_dict)
            session.add(user_address)
    user_detail.sqlmodel_update(new_data_dict)
    session.add(user_detail)
    session.commit()
    session.refresh(user_detail)
    return {"message": "Update Successfully"}

@profile_router.post("/profile/add_criteria")
def add_criteria(criteria_detail: CriteriaInDB, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    temp_statement = select(CriteriaInDB).where(CriteriaInDB.criteria_name==criteria_detail.criteria_name,CriteriaInDB.aadhaar_number==logged_user_pk)
    temp_info = session.exec(temp_statement).first()
    if temp_info != None:
        raise criteria_already_exist(criteria_detail.criteria_name)
    else:
        if criteria_detail.criteria_value.isdigit():
            criteria_detail.data_type = "Numeric"
        else:
            criteria_detail.data_type = "String"
        criteria_detail.aadhaar_number = logged_user_pk
        session.add(criteria_detail)
        session.commit()
        session.refresh(criteria_detail)
        return {"messsage": "Created Successfully"}

@profile_router.patch("/profile/edit_criteria")
def update_criteria(new_detail: CriteriaEdit, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    new_detail_dict = new_detail.model_dump(exclude_unset=True)
    if "criteria_name" not in new_detail_dict.keys() or new_detail_dict["criteria_name"].strip()=="":
        raise missiing_value_exception("criteria_name")
    elif "criteria_value" not in new_detail_dict.keys():
        raise missiing_value_exception(new_detail_dict["criteria_name"])
    temp_statement = select(CriteriaInDB).where(CriteriaInDB.criteria_name==new_detail_dict["criteria_name"],CriteriaInDB.aadhaar_number==logged_user_pk)
    temp_info = session.exec(temp_statement).first()
    if temp_info is None:
        raise criteria_not_found(new_detail_dict["criteria_name"])
    temp_info.sqlmodel_update(new_detail_dict)
    session.add(temp_info)
    session.commit()
    session.refresh(temp_info)
    return {"message": "Update Successful"}