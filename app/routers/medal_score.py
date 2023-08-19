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


@router.post("/create")
def create_medal(medal_score_employee: Medal_Score_Employee):
    
    if medal_score_employee.employee_id and medal_score_employee.game_id:
        insert_medal_user = insert_medal(medal_id=id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=create_medal)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Unable to create the medal for the user!"})


