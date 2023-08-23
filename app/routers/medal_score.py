from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_medal import insert_medal
from app.schemas.medal_score_employee import Medal_Score_Employee
from fastapi import APIRouter

router = APIRouter(
    prefix="/medal_score",
    tags=[
        "medal_score"
    ]
    
)

@router.get("/get/{medal_id}")
def get_medal(medal_score_employee: Medal_Score_Employee):
    
    if medal_score_employee.employee_id and medal_score_employee.game_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee doesn't have a medal!"})

    else:
        get_medal_user = get_medal(medal_id=medal_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_medal_user)



@router.post("/create")
def create_medal(medal_score_employee: Medal_Score_Employee):
    
    if medal_score_employee.employee_id and medal_score_employee.game_id:
        insert_medal_user = insert_medal(medal_id=medal_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=insert_medal_user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Unable to create the medal for the user!"})

@router.put("/update")
def update_medal(medal_score_employee: Medal_Score_Employee):
    
    if medal_score_employee.employee_id and medal_score_employee.game_id:
        update_medal_user = update_medal(medal_id=medal_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The medal has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This medal couldn't be deleted!"})