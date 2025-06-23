from fastapi import HTTPException,status

wrong_authentication = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

user_not_found = HTTPException(status_code=404, detail="User not found")

user_already_exist = HTTPException(status_code=409, detail="User with this aadhaar number already exists")

def criteria_already_exist(criteria_name: str):
    return HTTPException(
            status_code=409,
            detail=f"{criteria_name} Criteria already exists."
        )

def criteria_not_found(criteria_name: str):
    return HTTPException(
            status_code=404,
            detail=f"{criteria_name} Criteria not found"
        )

def missiing_value_exception(value_holder_name: str):
    return HTTPException(
            status_code=422,
            detail=f"Please enter your {value_holder_name}"
        )