from sqlmodel import SQLModel,Field,Relationship
from datetime import date
from enum import Enum

class Gender(str,Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class UserType(str,Enum):
    USER = "User"
    ADMIN = "Admin"

class UserBase(SQLModel):
    aadhaar_number: str = Field(primary_key=True)

class UserLoginRequest(UserBase):
    password: str
    user_type: UserType

class UserSignupRequest(UserLoginRequest):
    full_name: str
    dob: date
    gender: Gender
    mobile_number: int

class UserInDB(UserBase, table=True):
    full_name: str
    dob: date
    gender: Gender
    mobile_number: int
    marital_status: bool | None = None
    occupation: str | None = None
    annual_income: int | None = None
    annual_family_income: int | None = None
    bank_account_number: str | None = None
    caste_category: str | None = None
    is_disable: bool | None = None
    bpl: str | None = None
    hashed_password: str

    address_detail: "UserAddressInDB" = Relationship(back_populates="user")

class UserAddressInDB(SQLModel, table = True):
    aadhaar_number: str = Field(foreign_key="userindb.aadhaar_number", primary_key=True)
    state: str | None = None
    district: str | None = None
    village_or_city: str | None = None
    exact_address: str | None = None
    pincode: int | None = None

    user: "UserInDB" = Relationship(back_populates="address_detail")