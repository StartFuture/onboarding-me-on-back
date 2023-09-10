from app.dao import dao_tools as dao
from app.dao import dao_company
from app.schemas.category_tool import CategoryTool
from app.schemas.tool import Tool, EmployeeTool

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app import utils


router = APIRouter(
    prefix="/tool",
    tags=[
        "tool"
    ]
        )

@router.get("/")
def get_tools(company_id: int):
    
    company_exists = dao_company.verify_if_company_exists(company_id)
    
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
    tool_exists = dao.verify_tool_exists(name=tool.name)

    if tool_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"This tool is already registered!"})
    else:
        tool_registered = dao.insert_tool(tool)

        if tool_registered:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The tool has been registered!"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been registered!"})


@router.put("/update")
def modify_tool(tool: Tool):

    tool_exists = dao.verify_tool_exists(id_tool=tool.id_tool)
    tool.name = utils.string_to_lower(tool.name)

    if tool_exists:
        if tool.id_tool:
            tool_registered = dao.update_tool(tool)

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
    
    tool_exists = dao.verify_tool_exists(id_tool=tool_id)
     
    if not tool_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This tool dont exists!"})
    
    tool_deleted = dao.delete_tool(tool_id=tool_id, game_id=game_id)
    
    if tool_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The tool has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool has not been deleted!"})  
    
    
@router.post("/category/register")
def register_category_tool(category_tool: CategoryTool):

    category_exists = dao.verify_if_category_exists(category_name=category_tool.name)
    
    if category_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "The category already exists!"})
    
    category_registered = dao.insert_category_tool(category_tool)

    if category_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The category has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The category has not been registered!"})
    
    
@router.put("/category/update")
def modify_category_tool(category_tool: CategoryTool):
    
    category_exists = dao.verify_if_category_exists(category_id=category_tool.category_tool_id)
    
    if not category_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The category dont exists!"})
    
    
    if not category_tool.category_tool_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Missing category id!"})
    

    category_modified = dao.update_category_tool(category_tool)
    
    if category_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The category has been modified!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The category has not been modified!"})
    
    
    
@router.delete("/category/delete")
def del_category_tool(category_tool_id: int, company_id: int):
    
    category_exists = dao.verify_if_category_exists(category_id=category_tool_id)
    
    if not category_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The category dont exists!"})
    
    category_deleted = dao.delete_category_tool(category_tool_id=category_tool_id, company_id=company_id)

    if category_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The category has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The category has not been deleted!"})
    

@router.post("/linking")
def complete_tool(employee_tool: EmployeeTool):

    tool_exists = dao.verify_tool_exists(id_tool=employee_tool.tool_id)

    if tool_exists:
        tool_completed = dao.verify_tool_completed(tool_id=employee_tool.tool_id)

        if tool_completed:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This tool has already been completed!"})
        else:
            tool_linking = dao.linking_tool(employee_tool)

            if tool_linking:
                score_exists = dao.verify_score_tool_exists(dao.get_game_id_tool(employee_tool))

                if type(score_exists) == int:
                    if score_exists == 1:
                        score_update = dao.saving_tool_score(employee_tool, score_exists=True)
                        if score_update:
                            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The tool has been successfully completed!"})
                        else:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in score"})
                    elif score_exists == 0:
                        score_insert = dao.saving_tool_score(employee_tool)
                        if score_insert:
                            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The tool has been successfully completed!"})
                        else:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in score"})
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in score"})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool is not completed!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tool does not exist!"})


@router.get("/game/")
def game_tools_completed(gamefied_journey_id: int, employee_id: int):

    tool_count = dao.get_count_tools(gamefied_journey_id)

    if not tool_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tools were not found! "})
    
    game_tools_completed = dao.ended_game_tools(employee_id)

    if not game_tools_completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The completed tools were not found!"})
    
    if tool_count == game_tools_completed:
       return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The tool game has been successfully completed!"})
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "The tool game has not been completed!"})
        
