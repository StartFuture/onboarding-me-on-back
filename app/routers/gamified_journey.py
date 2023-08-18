from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_gamified_journey import insert_video_company, select_video_company, modify_video_company 
from app.schemas.gamified_journey import GamifiedJourney 
from fastapi import APIRouter


router = APIRouter(
    prefix="/gamified_journey",
    tags=[
        "gamified_journey"
    ]
    
                   )


@router.get("/get-video-company/{game_id}")
def get_video_company(id: int):
    
    video = dao.select_video_company(company_id=id)
        
    if video:
            return JSONResponse(status_code=status.HTTP_200_OK, content=video)
    else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have a video!"})

@router.post("/create")
def create_video_company(game_id: int, link: str):
    
    video = dao.insert_video_company(company_id=id)

    if video:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have a video!"})


@router.post("/update")
def update_video_company(game_id: int, new_link: str):
    
    video = dao.modify_video_company(company_id=id)

    if video:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The video has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have a video!"})