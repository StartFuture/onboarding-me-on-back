from app.dao import dao_tools as dao
from app.schemas.category_tool import CategoryTool

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app import utils
from app.schemas.tool import Tool
from app.dao.dao_tools import select_tools, insert_tool, update_tool, verify_tool_exists


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


@router.post("/register") 
def register_tool(tool: Tool):

    tool.name = utils.string_to_lower(tool.name)
    tool_exists = verify_tool_exists(name=tool.name)

    if tool_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"This tool is already registered!"})
    else:
        tool_registered = insert_tool(tool)

        if tool_registered:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The tool has been registered!"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been registered!"})


@router.put("/update")
def modify_tool(tool: Tool):

    tool_exists = verify_tool_exists(id_tool=tool.id_tool)
    tool.name = utils.string_to_lower(tool.name)

    if tool_exists:
        if tool.id_tool:
            tool_registered = update_tool(tool)

            if tool_registered:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Success updated!"})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been modified!"})
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Missing id tool!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"This tool is not registered!"}) 
     
    
@router.delete("/delete")
def del_tool(tool_id: int, game_id: int):   
    
    tool_exists = verify_tool_exists(id_tool=tool_id)
     
    if not tool_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This tool dont exists!"})
    
    tool_deleted = dao.delete_tool(tool_id=tool_id, game_id=game_id)
    
    
    if tool_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The tool has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been deleted!"})  
    
    
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