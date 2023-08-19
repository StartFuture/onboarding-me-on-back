from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao.dao_medal import select_medal, insert_medal, modify_medal
from app.schemas.medal import Medal 
from fastapi import APIRouter


router = APIRouter(
    prefix="/medal",
    tags=[
        "medal"
    ]
    
                   )


@router.get("/get-medal")
def get_medal(medal_id: int):
    
    medal_user = dao.select_medal(medal_id=id)
    
    if medal_user:
        return JSONResponse(status_code=status.HTTP_200_OK, content = medal_user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This user doesn't have a medal!"})

@router.post("/create-medal")
def create_medal(name: str, medal_id: int):
    insert_medal_user = dao.insert_medal(medal_id=id)
    
    if insert_medal_user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=insert_medal_user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This user doesn't have a medal!"})



@router.post("/update-medal")
def modify_medal(name: str, medal_id: int):
    modify_medal__user = dao.modify_medal(medal_id=id)
    
    if modify_medal__userr:
        return JSONResponse(status_code=status.HTTP_200_OK, content=modify_medal__user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This user doesn't have a medal!"})
