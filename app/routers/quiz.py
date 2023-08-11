from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


from app.dao import dao_quiz as dao
from app.schemas.quiz import Quiz



router = APIRouter(
    prefix="/quiz",
    tags=[
        "quiz"
    ]
        )



@router.get("/{company_id}")
def get_quiz(company_id: int):
    
    quiz = dao.select_quiz(company_id)
    
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
def modify_quiz(quiz: Quiz):

    list_alternative_id = []
    
    for alternative in quiz.alternatives:
        
        if alternative.alternative_id:
            list_alternative_id.append(alternative.alternative_id)
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Alternative id is required!"})
    
    
    game_id_exists = dao.verify_if_game_id_exists(quiz)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This game_id not exists!"})
    
    
    quiz_id_exists = dao.verify_if_quiz_id_exists(quiz)
    
    if not quiz_id_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This quiz_id not exists!"})
    
    
    alternative_id_exists = dao.verify_if_alternative_id_exists(list_alternative_id, quiz.quiz_id)
    
    if len(alternative_id_exists) == len(list_alternative_id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "This alternative_id not exists!"})



    quiz_modified = dao.update_quiz(quiz)

    
    if quiz_modified:
        alternative_modified = dao.update_alternative(quiz.alternatives, quiz.quiz_id)
    
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})
        
        
    if quiz_modified and alternative_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The quiz has been modified!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The quiz has not been modified!"})
    
