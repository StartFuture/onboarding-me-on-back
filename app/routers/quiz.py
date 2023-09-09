from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.dao import dao_quiz as dao
from app.dao import dao_employee
from app.dao import dao_company
from app.schemas.quiz import Quiz



router = APIRouter(
    prefix="/quiz",
    tags=[
        "quiz"
    ]
        )



@router.get("/")
def get_quiz(company_id: int):
    
    quiz = dao.select_quiz(company_id=company_id)
    
    if quiz:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have quiz!"})
    
    
@router.post("/register")
def register_quiz(quiz: Quiz):

    game_id_exists = dao.verify_if_game_id_exists(quiz)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game_id not exists!"})
    

    id_quiz = dao.insert_quiz(quiz)
    
    
    
    alternative_registered = dao.insert_alternatives(quiz.alternatives, id_quiz['id_quiz'])
    
    if id_quiz and alternative_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The quiz has not been registered!"})
    
    
@router.put("/update")
def modify_quiz(quiz: Quiz, company_id: int):

    list_alternative_id = []
    
    if not quiz.alternatives:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Alternative is required!"})
    
    
    for alternative in quiz.alternatives:
        
        if alternative.alternative_id:
            list_alternative_id.append(alternative.alternative_id)
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Alternative id is required!"})
    
    
    game_id_exists = dao.verify_if_game_id_exists(quiz)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This game_id not exists!"})
    
    
    quiz_id_exists = dao.verify_if_quiz_id_exists(quiz=quiz, company_id=company_id)
    
    if not quiz_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This quiz_id not exists!"})
    
    
    alternative_id_exists = dao.verify_if_alternative_id_exists(list_alternative_id, quiz.quiz_id)
    
    if len(alternative_id_exists) != len(list_alternative_id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This alternative_id not exists!"})


    quiz_modified = dao.update_quiz(quiz)

    
    if quiz_modified:
        alternative_modified = dao.update_alternative(quiz.alternatives, quiz.quiz_id)
    
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})
        
        
    if quiz_modified and alternative_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The quiz has been modified!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The quiz has not been modified!"})


@router.delete("/delete")
def delete_quiz(quiz_id: int, game_id: int, company_id: int):
    
    game_id_exists = dao.verify_if_game_id_exists(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This game_id not exists or dont have this quiz!"})
    
    
    quiz_id_exists = dao.verify_if_quiz_id_exists(quiz_id=quiz_id, company_id=company_id)
    
    if not quiz_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This quiz_id not exists!"})
    
    
    quiz_deleted = dao.delete_quiz_alternative(quiz_id=quiz_id, game_id=game_id)  
    
    if quiz_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The quiz has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This quiz still has alternatives! (delete them first)"})


@router.delete("/alternative/delete")
def del_alternative(alternative_id: int, quiz_id: int):
    
    alternative_list = [alternative_id]
    
    alternative_id_exists = dao.verify_if_alternative_id_exists(alternative_list, quiz_id)
    
    if len(alternative_id_exists) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This alternative_id not exists!"})
    
    
    alternative_deleted = dao.delete_alternative(alternatives = alternative_list, quiz_id = quiz_id)

    
    if alternative_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The alternative has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The alternative has not been deleted!"})


@router.get("/next/{employee_id}")
def return_next_quiz(employee_id: int):

    employee_exists = dao_employee.verify_employee_exists(employee_id)

    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The employee doesn't exist!"})

    quizzes_completed = dao.select_quiz_id_completed(employee_id)

    if not quizzes_completed:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail={"msg": "The complete quizzes could not be found!", "next_quiz" : None, "completed" : False})
    
    quiz_id = dao.select_next_quiz_id(employee_id, quizzes_completed)

    if not quiz_id:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"msg": "All quizzes completed!", "next_quiz" : None, "completed" : True})
    else:
        next_quiz = dao.select_next_quiz(quiz_id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Next quiz", "next_quiz" : next_quiz})
    

@router.get("/game_id")
def get_quiz_game_id(company_id: int):
    
    game = dao.select_quiz_game_id(company_id=company_id)
    
    if game: 
        return JSONResponse(status_code=status.HTTP_200_OK, content=game)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This game doesn't exist!"})