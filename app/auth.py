from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from app.dao import dao_auth as dao
from app.dao.dao_company import verify_company_exists_by_email
from app.parameters import ALGORITHM, SECRET_KEY


oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_token(token: dict = Depends(oauth)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
    except JWTError:
        raise HTTPException(detail={'msg': 'missing token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
    
    else:
        
        if payload['type'] == 'company':
            verify_company = verify_token_company(token)
            return verify_company
            
        elif payload['type'] == 'employee':
            verify_employee = verify_token_employee(token)
            return verify_employee
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Not authorized!"})
        

def verify_token_company(token: dict = Depends(verify_token)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
    except JWTError:
        raise HTTPException(detail={'msg': 'missing token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
    
    else:
        
        company_exists = verify_company_exists_by_email(payload['company_email'])

        if not company_exists:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        token_revoked = dao.select_revoked_token(user_id=payload['sub'], token=token)
        
        if token_revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        type_is_valid = True if payload['type'] == 'company' else False
        
        if not type_is_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Not authorized!"})
        
        return payload
    

def verify_token_employee(token: dict = Depends(verify_token)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
    except JWTError:
        raise HTTPException(detail={'msg': 'missing token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
    
    else:
        
        company_exists = verify_company_exists_by_email(payload['company_email'])

        if not company_exists:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        token_revoked = dao.select_revoked_token(user_id=payload['sub'], token=token)
        
        if token_revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "User or passwords incorrects!"})
        
        type_is_valid = True if payload['type'] == 'employee' else False
        
        if not type_is_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Not authorized!"})
        
        return payload