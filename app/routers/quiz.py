from app.dao.dao_quiz import select_quiz, insert_quiz, insert_alternatives, update_quiz, update_alternative
from app.schemas.quiz import Quiz, Alternative

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/quiz",
    tags=[
        "quiz"
    ]
        )



@router.get("/{company_id}")
def get_quiz(company_id: int):
    
    quiz = select_quiz(company_id)
    
    if quiz:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have quiz!"})
    
    
@router.post("/")
def register_quiz(quiz: Quiz):

    id_quiz = insert_quiz(quiz)
    alternative_registered = insert_alternatives(quiz.alternatives, id_quiz['id_quiz'])

    if id_quiz and alternative_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The quiz has not been registered!"})
    
    
    
@router.put("/")
def modify_quiz(quiz: Quiz):
    
    quiz_modified = update_quiz(quiz)

    if quiz_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz_modified)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The quiz has not been modified!"})
    
    
@router.put("/alternative")
def modify_alternative(alternative: Alternative):
    
    alternative_modified = update_alternative(alternative)

    if alternative_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content=alternative_modified)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The alternative has not been modified!"})