from routes import *
from constants import demodata
from fastapi import Depends
from auth.jwt_service import verifyToken

router  = APIRouter(
    dependencies=[Depends(verifyToken)]
)


@router.get('/profile/{aadhaar_number}', status_code=status.HTTP_200_OK)   ## here mention the return type
async def get_profile(aadhaar_number : int):
    print('inside profile route')
    user = demodata.demo_user_data.get(aadhaar_number)  ## replace this with db searching and filtering logic
    if not user:
        raise http_exceptions.Exceptions['user_not_found_Exception']
    return response_emitter.success_response('user retreived succesfully', data=user)

