from app.dao.dao_gamified_journey import insert_video_company, select_video_company, update_video_company_db 
from app.schemas.gamified_journey import GamifiedJourney 
from fastapi import APIRouter


router = APIRouter(
    prefix="/gamified_journey",
    tags=[
        "gamified_journey"
    ]
    
                   )


@router.get("/get-video-company/{id}")
def get_video_company(id: int):
    video_company = select_video_company(id=id)
    return video_company

@router.post("/create")
def create_video_company(gamified_journey: GamifiedJourney):
    insert_video_company()
    return gamified_journey

@router.post("/update")
def update_video_company(gamified_journey: GamifiedJourney):
    update_video_company_db()
    return gamified_journey
