from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_medal import insert_medal, select_medal_by_employee, select_medal_by_game, select_score_by_employee
from app.schemas.medal_score_employee import Medal_Score_Employee
from fastapi import APIRouter

router = APIRouter(
    prefix="/medal_score",
    tags=[
        "medal_score"
    ]
    
)

@router.get("/get/{employee_id}")
def get_medal(employee_id: int):
    
    medal = select_medal_by_employee(employee_id=employee_id)
    
    if medal:
        return JSONResponse(status_code=status.HTTP_200_OK, content=medal)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee doesn't have a medal!"})


@router.post("/create")
def create_medal(medal_score_employee: Medal_Score_Employee):
    
    medal_id = select_medal_by_game(game_id=medal_score_employee.game_id)
    
    if not medal_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Game_id doesn't exists!"})
    
    score_id = select_score_by_employee(employee_id=medal_score_employee.employee_id)
    
    if not score_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "employee_id doesn't exists!"})
    
    success = insert_medal(medal_id=medal_id["id"], score_id=score_id["id"]) 
    
    if success:
        return JSONResponse(status_code=status.HTTP_200_OK, content=success)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Unable to create the medal for the user!"})