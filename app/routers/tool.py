from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_tools import select_tool


router = APIRouter(
    prefix="/tool",
    tags=[
        "tool"
    ]
        )

@router.get("/{company_id}")
def get_tool(company_id: int):
    
    tool = select_tool(company_id)
    
    if tool:
        return JSONResponse(status_code=status.HTTP_200_OK, content=tool)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have tools!"})
