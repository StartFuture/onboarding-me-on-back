from app.dao.dao_quiz import select_quiz

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