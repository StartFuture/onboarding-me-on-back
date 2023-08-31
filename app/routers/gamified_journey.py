from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_gamified_journey import insert_video_company, select_video_company, modify_video_company 
from app.dao.dao_company import select_company
from app.schemas.gamified_journey import GamifiedJourney 
from fastapi import APIRouter


router = APIRouter(
    prefix="/game_journey",
    tags=[
        "gamified_journey"
    ]
    
)


@router.get("/get-video/{company_id}")
def get_video_company(company_id: int):

    company = select_company(company_id)
    
    if company == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't exist!"})

    else:
        video = select_video_company(company_id=company_id)
        
        if not video:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company video doesn't exist!"})
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=video)


@router.post("/create")
def create_video_company(gamifiedJourney: GamifiedJourney):
    
    company = select_company(gamifiedJourney.company_id)
    
    if company:
        video = insert_video_company(company_id=gamifiedJourney.company_id, link=gamifiedJourney.welcome_video_link)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company's video can't be created"})
    else:
        video = modify_video_company(company_id=gamifiedJourney.company_id, new_link=gamifiedJourney.welcome_video_link)
        return JSONResponse(status_code=status.HTTP_200_OK, content=video)


@router.put("/update")
def update_video_company(company_id: int, new_link: str):
    
    video = modify_video_company(company_id=company_id, new_link=new_link)
    
    if company_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't exist!"})

    if video:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The video has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't have a video!"})