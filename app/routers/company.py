from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.company import Company 
from app.dao.dao_company import select_company

router = APIRouter(
    prefix="/company",
    tags=[
        "company"
    ]
)


@router.get("/{id}")
def get_company(id):
    
    company = select_company(company_id=id)
    
    if company:
        return JSONResponse(status_code=status.HTTP_200_OK, content=company)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't exists!"})

