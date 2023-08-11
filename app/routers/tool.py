from app.dao import dao_tools as dao
from app.schemas.category_tool import CategoryTool

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/tool",
    tags=[
        "tool"
    ]
        )

@router.get("/{company_id}")
def get_tools(company_id: int):
    
    company_exists = dao.verify_if_company_exists(company_id)
    
    if not company_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't exists!"})
    
    tool = dao.select_tools(company_id)
    
    if tool:
        return JSONResponse(status_code=status.HTTP_200_OK, content=tool)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have tools!"})
    
    
    
@router.get("/category/{tool_id}")
def get_category_tool(tool_id: int):
    
    category_tool = dao.select_category_tool(tool_id)
    
    if category_tool:
        return JSONResponse(status_code=status.HTTP_200_OK, content=category_tool)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have this tool_id!"})
    
    
@router.post("/category/register")
def register_category_tool(category_tool: CategoryTool):

    category_exists = dao.verify_if_category_exists(category_tool)
    
    if category_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "The category already exists!"})
    
    category_registered = dao.insert_category_tool(category_tool)

    if category_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The category has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The category has not been registered!"})