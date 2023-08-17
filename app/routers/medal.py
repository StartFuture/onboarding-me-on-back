from app.dao.dao_medal import select_medal, insert_medal, modify_medal
from app.schemas.medal import Medal 
from fastapi import APIRouter


router = APIRouter(
    prefix="/medal",
    tags=[
        "medal"
    ]
    
                   )


@router.get("/get-medal/{id}")
def get_medal(name: str, game_id: int):
    get_medal_user = select_medal(game_id=id)
    return get_medal_user

@router.post("/create-medal")
def create_medal(name: str, game_id: int):
    insert_medal_user = insert_medal(game_id=id)
    return insert_medal_user 

@router.post("/update-medal")
def modify_medal(name: str, game_id: int):
    modify_medal__user = modify_medal(game_id=id)
    return modify_medal__user
