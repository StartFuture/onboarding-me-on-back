from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.schemas.company import Company 
from app.dao import dao_company as dao
from app.auth import verify_token_company
from app.utils import create_hash

router = APIRouter(
    prefix="/company",
    tags=[
        "company"
    ]
)


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
    
    company.password = create_hash(company.password)
    company.cnpj = company.cnpj.replace('-', '').replace('/', '').replace('.', '')
    
    company_registered = dao.insert_company(company)
    
    if company_registered:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully created"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in company"})
    
    
@router.put("/update")
def modify_company(company: Company, token: dict = Depends(verify_token_company)):
    
    company_exists = dao.verify_if_company_exists(company.company_id)
    
    if not company_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Company dont exists!"})
    
    company.password = create_hash(company.password)
    company.cnpj = company.cnpj.replace('-', '').replace('/', '').replace('.', '')
    
    company_updated = dao.update_company(company)
    
    if company_updated:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in company"})

    
@router.delete("/delete")
def del_company(company_id: int):
    
    company_exists = dao.verify_if_company_exists(company_id)
    
    if not company_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Company dont exists!"})
    
    company_deleted = dao.delete_company(company_id)
    
    if company_deleted:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully deleted"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in company"})
    