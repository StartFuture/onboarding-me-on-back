from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.utils import validate_password
from app.dao.dao_company import verify_company_exists_by_email
from app.parameters import ACCESS_TOKEN_EXPIRES, ALGORITHM, SECRET_KEY
from app.auth import verify_token


router = APIRouter(
    prefix="/auth",
    tags=[
        "auth"
    ]
)



@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):

    company_user = verify_company_exists_by_email(user.username)
    
    if not company_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    valid_password = validate_password(password=user.password, password_hash=company_user['company_password'])
    
    if not valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

    payload = {
        'company_email': company_user['email'],
        'sub': str(company_user['id']),
        'exp': datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRES)),
        'type': 'company'
     }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token})


@router.post('/token_health')
def token_health_check(token: dict = Depends(verify_token)):
    
    if token['type'] == 'company':

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'company'},
            status_code=status.HTTP_200_OK
            )
        
    if token['type'] == 'employee':

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'employee'},
            status_code=status.HTTP_200_OK
            )
