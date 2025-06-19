from sqlmodel import SQLModel
from datetime import date
from Database.ORM_Models.auth_models import Gender

class ProfileExpose(SQLModel):
    aadhaar_number: str
    full_name: str
    dob: date
    gender: Gender
    mobile_number: int
    marital_status: bool | None
    occupation: str | None
    annual_income: int | None
    annual_family_income: int | None
    bank_account_number: str | None
    caste_category: str | None
    is_disable: bool | None
    bpl: str | None