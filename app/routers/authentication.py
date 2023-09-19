from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.utils import validate_password
from app.dao.dao_company import verify_company_exists_by_email, select_company_health_jwt
from app.dao.dao_employee import verify_employee_exists_by_email, select_employee_health_jwt
from app.dao.dao_auth import insert_revoked_tokens
from app.parameters import ACCESS_TOKEN_EXPIRES, ALGORITHM, SECRET_KEY
from app.auth import verify_token_health, return_token


router = APIRouter(
    prefix="/auth",
    tags=[
        "auth"
    ]
)



@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), type: str = Query(pattern=r'company|employee', description="User type")):
    
    
    if type == 'company':
        
        company_user = verify_company_exists_by_email(user.username)
        
        if not company_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        valid_password = validate_password(password=user.password, password_hash=company_user['company_password'])
        
        if not valid_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

        payload = {
            'company': company_user['id'],
            'email': company_user['email'],
            'sub': str(company_user['id']),
            'exp': datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRES)),
            'type': 'company'
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token})

    if type == 'employee':
        
        employee_user = verify_employee_exists_by_email(user.username)
        
        if not employee_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        valid_password = validate_password(password=user.password, password_hash=employee_user['employee_password'])
        
        if not valid_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

        payload = {
            'company': employee_user['company_id'],
            'email': employee_user['email'],
            'sub': str(employee_user['id']),
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

        company = select_company_health_jwt(payload["sub"])

        if not company:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail={"msg": "User or passwords incorrects!"}
            )

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'company', 'company': company},
            status_code=status.HTTP_200_OK
            )
        
    if payload['type'] == 'employee':
        
        employee = select_employee_health_jwt(payload["sub"])

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail={"msg": "User or passwords incorrects!"}
            )

        return JSONResponse(
            content={'msg': 'token is valid', 'type': 'employee', 'employee': employee},
            status_code=status.HTTP_200_OK
            )
