from app.dao.dao_gamified_journey import insert_video_company, select_video_company, modify_video_company 
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
def create_video_company(id: int, link: str):
    video_insert_company = insert_video_company(id=id)
    return video_insert_company

@router.post("/update")
def update_video_company(id: int, new_link: str):
    video_update_company = modify_video_company(id=id)
    return video_update_company
