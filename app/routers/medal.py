from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse



from app.dao import dao_medal as dao
from app.dao.dao_quiz import verify_if_game_id_exists

router = APIRouter(
    prefix="/medal",
    tags=[
        "medal"
    ]
        )


@router.get("/")
def get_medal(id, game_id: int):
    
    medal = dao.select_medal(id, game_id)
    
    if medal:
        return JSONResponse(status_code=status.HTTP_200_OK, content=medal)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This medal does not exists!"})    


@router.post("/register")
def create_medal(name, image: str, game_id: int):
    
    game_id_exists = verify_if_game_id_exists(game_id=game_id)
    
    if not game_id_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game_id not exists!"})
    
    medal_created = dao.insert_medal(name, image, game_id)
    
    if medal_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg":"The medal has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have quiz!"})
    

@router.put("/update")
def modify_medal(medal_id: int, name, image: str):
    
    medal_exists = dao.verify_if_medal_exists(medal_id)
    
    if not medal_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This medal does not exists!"})
    
    medal_updated = dao.update_medal(medal_id, name, image)
    
    if medal_updated:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The medal has been modified!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in medal"})
    
    
@router.delete("/delete")
def del_medal(medal_id: int):
    
    medal_exists = dao.verify_if_medal_exists(medal_id)
    
    if not medal_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This medal does not exists!"})
    
    medal_deleted = dao.delete_medal(medal_id)
    
    if medal_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The medal has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in medal"})
    

