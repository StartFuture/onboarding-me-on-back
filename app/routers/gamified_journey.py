from fastapi import APIRouter,status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao.dao_gamified_journey import insert_video_company, select_video_company, modify_video_company, delete_video
from app.dao.dao_company import select_company
from app.schemas.gamified_journey import GamifiedJourney 
from app.utils import fix_video_link
from app.auth import verify_token_company, verify_token_employee_or_company

router = APIRouter(
    prefix="/game_journey",
    tags=[
        "gamified_journey"
    ]
    
)


@router.get("/get-video")
def get_video_company(payload: str = Depends(verify_token_employee_or_company)):
    
    print(payload)

    video = select_video_company(company_id=payload['company'])
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company video doesn't exist!"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=video)


@router.post("/create")
def create_video_company(gamifiedJourney: GamifiedJourney, payload: str = Depends(verify_token_company)):
    
    gamifiedJourney.welcome_video_link = fix_video_link(gamifiedJourney.welcome_video_link)
    
    video_created = insert_video_company(company_id=payload['sub'], link=gamifiedJourney.welcome_video_link)
    
    if video_created:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'msg': 'Successfully created'})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in video!"})

@router.put("/update")
def update_video_company(new_link: str, payload: str = Depends(verify_token_company)):
    
    new_link = fix_video_link(new_link)
     
    video_updated = modify_video_company(company_id=payload['sub'], new_link=new_link)

    if video_updated:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The video has been updated!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't have a video!"})


@router.delete("/delete")
def delete_video_company(payload: str = Depends(verify_token_company)):
    
    video_deleted = delete_video(company_id=payload['sub'])
    
    if video_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The video has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company doesn't have a video!"})

