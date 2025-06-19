from fastapi import HTTPException,status

wrong_authentication = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

user_not_found = HTTPException(status_code=404, detail="User not found")

user_already_exist = HTTPException(status_code=409, detail="User with this aadhaar number already exists")