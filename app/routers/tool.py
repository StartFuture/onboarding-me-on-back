from app.dao.dao import connect_database
from app.dao.dao_tools import select_tool

from fastapi import APIRouter


router = APIRouter(
    prefix="/tool",
    tags=[
        "tool"
    ]
        )

@router.get("/{company_id}")
def get_tool(company_id: int):
    
    tool = select_tool(company_id)
    
    return tool
