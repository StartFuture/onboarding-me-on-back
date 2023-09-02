from jose import jwt, JWTError
from fastapi import APIRouter, Depends

router = APIRouter(
    
    prefix="/authentication",
    tags=[
        "authentication"
    ]
)



@router.get("/")
def login():
    pass