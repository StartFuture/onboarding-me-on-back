from app.dao.dao_quiz import select_quiz, insert_quiz, insert_alternative, update_quiz, update_alternative
from app.schemas.quiz import Quiz
from app.schemas.alternative import Alternative

from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/quiz",
    tags=[
        "quiz"
    ]
        )


def validate_quiz_type(quiz: Quiz):
    
    if quiz.quiz_type != "culture" and quiz.quiz_type != "principle":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The quiz_type must be: 'culture' or 'principle'!"})

def validate_alternative_isanswer(alternative: Alternative):
   
    if alternative.is_answer != 1 and alternative.is_answer != 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The is_answer must be: '0' or '1'!"})



@router.get("/{company_id}")
def get_quiz(company_id: int):
    
    quiz = select_quiz(company_id)
    
    if quiz:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have quiz!"})
    
    
@router.post("/")
def register_quiz(quiz: Quiz):
    
    validate_quiz_type(quiz)

    quiz_registered = insert_quiz(quiz)

    if quiz_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz_registered)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The quiz has not been registered!"})
    
    
    
@router.post("/alternative")
def register_alternative(alternative: Alternative):
    
    validate_alternative_isanswer(alternative)

    alternative_registered = insert_alternative(alternative)

    if alternative_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content=alternative_registered)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The alternative has not been registered!"})
    
    
@router.put("/")
def modify_quiz(quiz: Quiz):
    
    validate_quiz_type(quiz)

    quiz_modified = update_quiz(quiz)

    if quiz_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content=quiz_modified)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The quiz has not been modified!"})
    
    
@router.put("/alternative")
def modify_alternative(alternative: Alternative):

    validate_alternative_isanswer(alternative)
    
    alternative_modified = update_alternative(alternative)

    if alternative_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content=alternative_modified)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The alternative has not been modified!"})