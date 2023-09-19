from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.utils import validate_password
from app.dao.dao_auth import insert_revoked_tokens
from app.parameters import ACCESS_TOKEN_EXPIRES, ALGORITHM, SECRET_KEY
from app.auth import verify_token_health, return_token, return_token_type


router = APIRouter(
    prefix="/auth",
    tags=[
        "auth"
    ]
)



@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):
    
    
    type, userdata = return_token_type(user.username)
    
    
    if type == 'company':
        
        valid_password = validate_password(password=user.password, password_hash=userdata['company_password'])
        
        if not valid_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

        payload = {
            'company': userdata['id'],
            'email': userdata['email'],
            'sub': str(userdata['id']),
            'exp': datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRES)),
            'type': 'company'
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token})

    if type == 'employee':
        
        valid_password = validate_password(password=user.password, password_hash=userdata['employee_password'])
        
        if not valid_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

        payload = {
            'company': userdata['company_id'],
            'email': userdata['email'],
            'sub': str(userdata['id']),
            'exp': datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRES)),
            'type': 'employee'
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token})
        
        
@router.post("/logout")
def logout(token: str = Depends(return_token)):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    
    revoked_token = insert_revoked_tokens(user_id=payload['sub'], token=token)
    
    if revoked_token:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The token has been revoked!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "The token has not been revoked!"}) 
    

@router.post('/token_health')
def token_health_check(payload: dict = Depends(verify_token_health)):
    
    if payload['type'] == 'company':

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'company'},
            status_code=status.HTTP_200_OK
            )
        
    if payload['type'] == 'employee':

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'employee'},
            status_code=status.HTTP_200_OK
            )
