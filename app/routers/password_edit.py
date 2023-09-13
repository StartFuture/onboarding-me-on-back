from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from app.utils import create_hash, validate_password
from app.auth import verify_token
from app.dao import dao_password_edit as dao

router = APIRouter(
    prefix="/password",
    tags=[
        "password"
    ]
)


@router.post('/password_edit')
def password_edit(current_password: str, new_password: str, token: str = Depends(verify_token)):
    
    id_user = token["sub"]

    new_password = create_hash(password=new_password)
    current_password = current_password
    
    result_password = dao.select_company_password(id_user)
    
    if not result_password:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Password user not found.')
    
    password_matches = validate_password(password=current_password, password_hash=result_password['company_password'])
    
    if not password_matches:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password.')
     
    updated_password = dao.update_password(new_password=new_password, user_id=id_user)
    
    if updated_password:
           return JSONResponse(status_code=status.HTTP_200_OK, content='Password successfully updated.')
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to update password')
        