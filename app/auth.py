from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.dao import dao_auth as dao
from app.dao.dao_company import verify_company_exists_by_email
from app.dao.dao_employee import verify_employee_exists_by_email
from app.parameters import ALGORITHM, SECRET_KEY


oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


def return_token(token: dict = Depends(oauth)):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    
    token_revoked = dao.select_revoked_token(user_id=payload['sub'], token=token)
        
    if token_revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
    return token
    

def verify_token(token: dict = Depends(oauth)):
    
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        if payload['type'] != 'company' and payload['type'] != 'employee':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Not authorized!"})
        
        token_revoked = dao.select_revoked_token(user_id=payload['sub'], token=token)
    
        if token_revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        return payload
        
    except JWTError:
        raise HTTPException(detail={'msg': 'missing token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
    
    
def verify_token_company(payload: dict = Depends(verify_token)):

    company_exists = verify_company_exists_by_email(payload['company_email'])

    if not company_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload
    

def verify_token_employee(payload: dict = Depends(verify_token)):
        
    employee_exists = verify_employee_exists_by_email(payload['email'])
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload


def verify_token_employee_or_company(payload: dict = Depends(verify_token)):
        
    employee_exists = verify_employee_exists_by_email(payload['email'])
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    company_exists = verify_company_exists_by_email(payload['company_email'])

    if not company_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload