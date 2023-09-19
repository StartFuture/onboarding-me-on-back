from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.dao import dao_auth as dao
from app.dao.dao_company import verify_company_exists_by_email
from app.dao.dao_employee import verify_employee_exists_by_email
from app.parameters import ALGORITHM, SECRET_KEY


oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")



def return_token_type(username: str):
    
    company_user = verify_company_exists_by_email(username)
    
    if company_user:
        usertype = 'company'
        
        return usertype, company_user
    
    employee_user = verify_employee_exists_by_email(username)
        
    if employee_user:
        usertype = 'employee'
        
        return usertype, employee_user   

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})


def return_token(token: dict = Depends(oauth)):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    
    token_revoked = dao.select_revoked_token(user_id=payload['sub'], token=token)
        
    if token_revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
    return token
    

def verify_token_health(token: dict = Depends(oauth)):
    
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
        
        
def verify_token(token: dict):
    
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
    
    
def verify_token_company(token: dict = Depends(oauth)):
    
    payload = verify_token(token)
    
    if payload['type'] != 'company':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})

    company_exists = verify_company_exists_by_email(payload['email'])

    if not company_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload
    

def verify_token_employee(token: dict = Depends(oauth)):
    
    payload = verify_token(token)
    
    if payload['type'] != 'employee':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    employee_exists = verify_employee_exists_by_email(payload['email'])
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload


def verify_token_employee_or_company(token: dict = Depends(oauth)):
    
    payload = verify_token(token)
    
    if payload['type'] != 'employee' and payload['type'] != 'company':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
     
     
    if payload['type'] == 'employee':
        
        employee_exists = verify_employee_exists_by_email(payload['email'])
        if not employee_exists:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    if payload['type'] == 'company':
        
        company_exists = verify_company_exists_by_email(payload['email'])
        if not company_exists:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
    
    return payload