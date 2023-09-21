from fastapi import APIRouter,status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao import dao_medal as dao
from app.dao.dao_quiz import verify_if_game_exists_in_company
from app.auth import verify_token_company

router = APIRouter(
    prefix="/medal",
    tags=[
        "medal"
    ]
        )


@router.get("/by-company")
def get_medal(payload: str = Depends(verify_token_company)):
    
    medal = dao.select_medals(company_id=payload['sub'])
    
    if medal:
        return JSONResponse(status_code=status.HTTP_200_OK, content=medal)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This medal does not exists!"})    


@router.post("/register")
def create_medal(name, image: str, game_id: int, payload: str = Depends(verify_token_company)):
    
    ids_list = []
    
    game_ids = verify_if_game_exists_in_company(company_id=payload['sub'])
    
    for id in game_ids:
        ids_list.append(id['id'])
        
    if game_id not in ids_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This game_id not exists!"})
 
    medal_created = dao.insert_medal(name, image, game_id)
    
    if medal_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg":"The medal has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have quiz!"})
    

@router.put("/update")
def modify_medal(medal_id: int, name, image: str, payload: str = Depends(verify_token_company)):
    
    ids_list = []
    
    company_medals = dao.select_medals(company_id=payload['sub'])
    
    for medal in company_medals:
        ids_list.append(medal['id'])
        
    if medal_id not in ids_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This medal_id not exists!"})
    
    medal_updated = dao.update_medal(medal_id, name, image)
    
    if medal_updated:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The medal has been modified!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in medal"})
    
    
@router.delete("/delete")
def del_medal(medal_id: int, payload: str = Depends(verify_token_company)):
    
    ids_list = []
    
    company_medals = dao.select_medals(company_id=payload['sub'])
    
    for medal in company_medals:
        ids_list.append(medal['id'])
        
    if medal_id not in ids_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This medal_id not exists!"})
    
    medal_deleted = dao.delete_medal(medal_id)
    
    if medal_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The medal has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This medal does not exists!"})
    

