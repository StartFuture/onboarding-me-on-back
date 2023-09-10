from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_gamified_journey import insert_video_company, select_video_company, modify_video_company, delete_video
from app.dao.dao_company import select_company
from app.schemas.gamified_journey import GamifiedJourney 


router = APIRouter(
    prefix="/game_journey",
    tags=[
        "gamified_journey"
    ]
    
)


@router.get("/get-video/")
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
    
    if not company:
        video = insert_video_company(company_id=gamifiedJourney.company_id, link=gamifiedJourney.welcome_video_link)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company's video can't be created"})
    else:
        video = modify_video_company(company_id=gamifiedJourney.company_id, new_link=gamifiedJourney.welcome_video_link)
        return JSONResponse(status_code=status.HTTP_200_OK, content=video)


@router.put("/update")
def update_video_company(company_id: int, new_link: str):
    
    company = select_company(company_id)
    
    if company == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't exist!"})
    
    video = modify_video_company(company_id=company_id, new_link=new_link)

    if video:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The video has been updated!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't have a video!"})


@router.delete("/delete")
def delete_video_company(company_id: int):
    
    company = select_company(company_id)

    if company == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't exist!"})
    
    delete_video(company_id=company_id)
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    

