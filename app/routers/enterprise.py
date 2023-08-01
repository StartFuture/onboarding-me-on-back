from app.dao.dao import connect_database
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
    connect_database()
    return enterprise
