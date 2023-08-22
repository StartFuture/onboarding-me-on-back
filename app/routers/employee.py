from app.dao import dao_employee as dao
from app.dao.dao_quiz import verify_if_quiz_id_exists, verify_if_game_id_exists
from app.schemas.quiz import EmployeeAlternative

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/employee",
    tags=[
        "employee"
    ]
        )


@router.get("/score")
def get_final_score(employee_id: int, game_id: int):
    
    employee_exists = dao.verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})  
      
    game_id_exists = verify_if_game_id_exists(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    
    
    total_score = dao.get_total_score(employee_id, game_id)
    
    if total_score or total_score == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=total_score)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Employee score not encountered!"})   
    
    

@router.post("/register/score") 
def register_score(employee_alternative: EmployeeAlternative, quiz_id: int):

    employee_exists = dao.verify_employee_exists(employee_alternative.employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    alternative_exists = dao.verify_alternative_exists(employee_alternative.alternative_id)
    
    if not alternative_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This alternative not exists!"})
    
    quiz_exists = verify_if_quiz_id_exists(quiz_id=quiz_id)
    
    if not quiz_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This quiz not exists!"})
    
    quiz_completed = dao.verify_quiz_completed(quiz_id)
    
    if quiz_completed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This quiz has already been completed!"})
    
    answer_registered = dao.insert_employee_answer(employee_alternative)
    
    if not answer_registered:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})
    
    score_exists = dao.verify_score_quiz_exists(dao.get_game_id_quiz(employee_alternative.alternative_id))

    if type(score_exists) != int:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in score"})
     
    if score_exists == 1:
        
        score_update = dao.saving_employee_score(employee_alternative, score_exists=True)
         
        if score_update:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The score has been updated!"})
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Answer incorrect!"}) 

    elif score_exists == 0:
    
        score_insert = dao.saving_employee_score(employee_alternative)
        
        if score_insert:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The score has been registered!"})
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Answer incorrect!"})

    