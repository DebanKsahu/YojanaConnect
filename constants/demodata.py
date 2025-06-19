from datetime import date
from enum import Enum


class Gender(str, Enum):
    MALE = ("MALE",)
    FEMALE = ("FEMALE",)
    OTHER = "OTHER"


demo_user_data = {
    123456789012: {
        "aadhaar_number": "123456789012",
        "full_name": "Abir Banerjee",
        "dob": date(2003, 7, 15),
        "gender": Gender.MALE,
        "mobile_number": 9876543210,
        "marital_status": False,
        "occupation": "Student",
        "annual_income": 120000,
        "annual_family_income": 300000,
        "bank_account_number": "1234567890",
        "caste_category": "General",
        "is_disable": False,
        "bpl": "No",
        "hashed_password": "$2b$12$somethinghashedhere",
        "address_detail": {
            "aadhaar_number": "123456789012",
            "district": "Kolkata",
            "village_or_city": "Kolkata",
            "exact_address": "221B Baker Street",
            "pincode": 700001,
        },
    }
}
