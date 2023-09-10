from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from passlib.context import CryptContext

from app.schemas.company import Company 
from app.dao import dao_company as dao


router = APIRouter(
    prefix="/company",
    tags=[
        "company"
    ]
)

crypt_context = CryptContext(schemes=['bcrypt'])


@router.get("/")
def get_company(company_id: int):
    
    company_exists = dao.verify_if_company_exists(company_id)
    
    if not company_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Company dont exists!"})
    
    company = dao.select_company(company_id)
    
    if company:
        return JSONResponse(status_code=status.HTTP_200_OK, content=company)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in company"})
    

@router.post("/register")
def create_company(company: Company):
    
    company_exists = dao.verify_company_exists_by_email(company.email)
    
    if company_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Company already exists!"})
    
    company.password = crypt_context.hash(company.password)
    
    company_registered = dao.insert_company(company)
    
    if company_registered:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully created"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in company"})
    
    