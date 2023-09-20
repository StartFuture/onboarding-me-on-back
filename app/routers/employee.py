from fastapi import APIRouter,status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao.dao_company import verify_if_company_exists
from app.schemas.employee import FeedBackEmployee

from app.dao import dao_employee as dao
from app.dao.dao_quiz import verify_if_quiz_id_exists, verify_if_game_id_exists_quiz
from app.schemas.quiz import EmployeeAlternative
from app.schemas.employee import Employee
from app.utils import create_hash
from app.auth import verify_token_company, verify_token_employee


router = APIRouter(
    prefix="/employee",
    tags=[
        "employee"
    ]
    
                   )



@router.get("/")
def get_employee(payload: dict = Depends(verify_token_employee)):
    
    employee = dao.select_employee(payload["sub"])
    
    if employee:
        return JSONResponse(status_code=status.HTTP_200_OK, content=employee)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in employee"})
    

@router.post("/register")
def create_employee(employee: Employee):
    
    employee_exists = dao.verify_employee_exists_by_email(employee.email)
    
    if employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Company already exists!"})
    
    employee.employee_password = create_hash(employee.employee_password)
    employee.phone_number = employee.phone_number.replace('-', '').replace('.', '').replace('(', '').replace(')', '')
    employee.cpf = employee.cpf.replace('-', '').replace('.', '')
    
    employee_registered = dao.insert_employee(employee)
    
    if employee_registered:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully created"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in employee"})
    
    
@router.put("/update")
def modify_employee(employee: Employee, payload: dict = Depends(verify_token_employee)):

    employee.employee_id = payload["sub"]
    employee.employee_password = create_hash(employee.employee_password)
    employee.phone_number = employee.phone_number.replace('-', '').replace('.', '').replace('(', '').replace(')', '')
    employee.cpf = employee.cpf.replace('-', '').replace('.', '')
    
    employee_updated = dao.update_employee(employee)
    
    if employee_updated:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in employee"})

    
@router.delete("/delete")
def del_employee(payload: dict = Depends(verify_token_employee)):
    
    employee_deleted = dao.delete_employee(payload["sub"])
    
    if employee_deleted:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully deleted"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in employee"})
    

@router.get("/feedback")
def get_feedback_employee(payload: dict = Depends(verify_token_employee)):

    feedback_list = dao.select_feedback(payload["company"])

    if feedback_list:
        return JSONResponse (status_code=status.HTTP_200_OK, content=feedback_list)
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have feedbacks"})


@router.get("/score")
def get_final_score_quiz(game_id: int, payload: dict = Depends(verify_token_employee)):  
      
    game_quiz_id_exists = verify_if_game_id_exists_quiz(game_id=game_id)
    
    if not game_quiz_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    
    
    total_score = dao.get_total_score(payload["sub"], game_id)
    
    if total_score or total_score == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=total_score)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Employee score not encountered!"})   
    

@router.post("/register/score") 
def register_score(employee_alternative: EmployeeAlternative, quiz_id: int, payload: dict = Depends(verify_token_employee)):

    employee_alternative.employee_id = payload["sub"]
    
    quiz_exists = verify_if_quiz_id_exists(quiz_id=quiz_id, company_id=payload["company"])
    
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
def get_employee_medals(game_id: int, payload: dict = Depends(verify_token_employee)):
      
    game_quiz_id_exists = verify_if_game_id_exists_quiz(game_id=game_id)
    
    if not game_quiz_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    
    
    employee_medals = dao.get_employee_medals(payload["sub"], game_id)
    
    if employee_medals:
        return JSONResponse(status_code=status.HTTP_200_OK, content=employee_medals)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee dont have medals!"})    
 
  
@router.post("/register/medal") 
def register_medal(game_id: int, payload: dict = Depends(verify_token_employee)): 
    
    score_id = dao.get_score_id_by_game_employee(game_id, payload["sub"])

    if not score_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Score not found!"})
    
    medal_score_registered = dao.insert_medal_score(employee_id=payload["sub"], game_id=game_id, score_id=score_id)
    
    if medal_score_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The medal has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error!"})
    
    
@router.get("/game/quiz/completed")
def game_quiz_completed(game_id: int, payload: dict = Depends(verify_token_employee)):
    
    game_id_exists = verify_if_game_id_exists_quiz(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game not exists!"})    

    quiz_completed = dao.finished_quiz_game(employee_id=payload["sub"], game_id=game_id)
     
    if quiz_completed:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The game has finished!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Incorrect answer!"})

@router.post("/register/feedback")
def create_feedback_employee(feedback_employee: FeedBackEmployee, payload: dict = Depends(verify_token_employee)):

    feedback_employee.employee_id = payload["sub"]

    feedback_exists = dao.verify_feedback_exists(feedback=feedback_employee)

    if feedback_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Feedback has already been recorded!"})

    is_register = dao.insert_feedback(feedback_employee)

    if is_register:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully feedback registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})


@router.get("/total-points-medals")
def return_total_points_medals(payload: dict = Depends(verify_token_employee)):
    
    total_points = dao.select_sum_total_points(payload["sub"])

    if not total_points:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The gamified journey points are null!"})

    medals_employee = dao.get_medals_by_employee_id(payload["sub"])

    if not medals_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The medals have not been found!"})
    
    if total_points and medals_employee:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total_points": total_points, "medals": medals_employee})
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Unknown error!"})