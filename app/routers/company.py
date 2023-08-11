from app.dao.dao import connect_database
from app.schemas.company import Company 
from fastapi import APIRouter


router = APIRouter(
    prefix="/company",
    tags=[
        "company"
    ]
    
                   )


@router.post("/")
def get_company(company: Company):
    connect_database()
    return company
