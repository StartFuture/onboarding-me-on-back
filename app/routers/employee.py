
from app.dao.dao_company import verify_if_company_exists
from app.schemas.employee import FeedBackEmployee

from app.dao import dao_employee as dao
from app.dao import dao_quiz 

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


@router.get("/feedback")
def get_feedback_employee(company_id : int):

    feedback_exists = verify_if_company_exists(company_id)

    if not feedback_exists:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't exists"})

    feedback_list = dao.select_feedback_company(company_id = company_id )

    if feedback_list:
        return JSONResponse (status_code=status.HTTP_200_OK, content=feedback_list)
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have feedbacks"})

@router.get("/score")
def get_final_score(employee_id: int, game_id: int, company_id):
    
    employee_exists = dao.verify_employee_exists(employee_id, company_id)
    
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
def register_score(employee_alternative: EmployeeAlternative, quiz_id: int, company_id: int):

    employee_exists = dao.verify_employee_exists(employee_alternative.employee_id, company_id=company_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"}) 
    
    quiz_exists = verify_if_quiz_id_exists(quiz_id=quiz_id, company_id=company_id)
    
    if not quiz_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This quiz not exists!"})
    
    alternative_exists = dao.verify_alternative_exists(alternative_id=employee_alternative.alternative_id, quiz_id=quiz_id)
    
    if not alternative_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This alternative not exists!"})
    
    quiz_completed = dao.verify_quiz_completed(quiz_id, employee_alternative.employee_id)
    
    if quiz_completed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This quiz has already been completed!"})
    
    answer_registered = dao.insert_employee_answer(employee_alternative)
    
    if not answer_registered:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})
    
    score_exists = dao.verify_score_quiz_exists(dao.get_game_id_quiz(employee_alternative.alternative_id), employee_id=employee_alternative.employee_id)

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


@router.get("/medal")
def get_employee_medals(employee_id: int, game_id: int, company_id: int):
    
    employee_exists = dao.verify_employee_exists(employee_id, company_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})  
      
    game_id_exists = verify_if_game_id_exists(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    
    
    employee_medals = dao.get_employee_medals(employee_id, game_id)
    
    if employee_medals:
        return JSONResponse(status_code=status.HTTP_200_OK, content=employee_medals)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee dont have medals!"})    
 
  
@router.post("/register/medal") 
def register_medal(score_id: int, game_id: int, employee_id: int, company_id: int): 
    
    employee_exists = dao.verify_employee_exists(employee_id, company_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"}) 
    
    medal_score_registered = dao.insert_medal_score(employee_id=employee_id, game_id=game_id, score_id=score_id)
    
    if medal_score_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The medal has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error!"})
    
    
@router.get("/game/quiz/completed")
def game_quiz_completed(employee_id: int, game_id: int, company_id: int):
    
    employee_exists = dao.verify_employee_exists(employee_id, company_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"}) 
    
    game_id_exists = verify_if_game_id_exists(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    

    quiz_completed = dao.finished_quiz_game(employee_id=employee_id, game_id=game_id)
     
    if quiz_completed:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The game has finished!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Incorrect answer!"})

@router.post("/register/feedback")
def create_feedback_employee(feedback_employee: FeedBackEmployee):

    employee_exists = dao.verify_employee_exists(feedback_employee.employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})

    is_register = dao.insert_feedback(feedback_employee)

    if is_register:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})
