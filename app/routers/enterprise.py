from app.schemas.enterprise import Enterprise 
from fastapi import APIRouter


router = APIRouter(
    prefix="/enterprise",
    tags=[
        "enterprise"
    ]
    
                   )


@router.post("/")
def get_enterprise(enterprise: Enterprise):
    return enterprise


