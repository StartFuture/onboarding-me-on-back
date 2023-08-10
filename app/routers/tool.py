from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.tool import Tool
from app.dao.dao_tools import select_tool, insert_tool, update_tool, verify_tool_exists


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


@router.post("/") 
def register_tool(tool: Tool):

    tool_exists = verify_tool_exists(name=tool.name)

    if tool_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"This tool is already registered!"})
    else:
        tool_registered = insert_tool(tool)

        if tool_registered:
            return JSONResponse(status_code=status.HTTP_200_OK, content=tool_registered)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been registered!"})


@router.put("/")
def modify_tool(tool: Tool):

    tool_exists = verify_tool_exists(id_tool=tool.id_tool)

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