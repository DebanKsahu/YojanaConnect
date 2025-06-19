from fastapi import HTTPException,status

Exceptions = {
    'user_not_found_Exception' : HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found'),
    'unauthorized_error' : HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are unauthorized to access the route'),
    'internal_server_error' : HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='internal server error')
}