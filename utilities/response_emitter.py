
def success_response(message: str , data=None):
    return {'message' : message , 'success' : True , 'data' : data}

def bad_response(message: str='Bad Response'):
    return {'message' : message , 'success' : False , 'data' : None}
