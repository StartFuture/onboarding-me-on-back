from app.dao.dao import connect_database
from app.dao.dao_quiz import select_quiz

from fastapi import APIRouter


router = APIRouter(
    prefix="/quiz",
    tags=[
        "quiz"
    ]
        )

@router.get("/{company_id}")
def get_quiz(company_id: int):
    
    quiz = select_quiz(company_id)
    
    return quiz