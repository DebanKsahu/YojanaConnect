from sqlmodel import SQLModel
from datetime import date
from Database.ORM_Models.auth_models import Gender, UserAddressInDB

class ProfileExpose(SQLModel):
    aadhaar_number: str
    full_name: str
    dob: date
    gender: Gender
    mobile_number: str
    marital_status: bool | None
    occupation: str | None
    annual_income: int | None
    annual_family_income: int | None
    bank_account_number: str | None
    caste_category: str | None
    is_disable: bool | None
    bpl: str | None
    user_address: UserAddressInDB | None

class ProfileEdit(SQLModel):
    full_name: str | None = None
    dob: date | None = None
    gender: Gender | None = None
    mobile_number: str | None = None
    marital_status: bool | None = None
    occupation: str | None = None
    annual_income: int | None = None
    annual_family_income: int | None = None
    bank_account_number: str | None = None
    caste_category: str | None = None
    is_disable: bool | None = None
    bpl: str | None = None
    user_address: UserAddressInDB | None = None