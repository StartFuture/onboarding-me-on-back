from app.dao import dao_welcomekit as dao
from app.utils import verify_is_allowed_file

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile

router = APIRouter(
    prefix="/welcomekit",
    tags=[
        "welcomekit"
    ]
)


@router.get("/welcomekit")
def get_welcome_kit_image(employee_id: int):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(employee_id=employee_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!"})
    
    welcome_kit_image = dao.select_welcome_kit_image(employee_id)
    
    if welcome_kit_image:
        return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit_image)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Image not found!"})
 
    
@router.post("/register/welcomekit")
async def register_welcome_kit(name: str, image: UploadFile = File(...)):
    
    is_allowed_file = verify_is_allowed_file(image.filename)
    
    if not is_allowed_file:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail={"msg": "This format file is not permited!"})
    
    welcome_kit_registered = await dao.insert_welcome_kit(welcome_kit_name=name, welcome_kit_image=image)
    
    if welcome_kit_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit has not been registered"})
    
    
@router.get("/welcomekit-item")    
def get_welcome_kit_item(welcome_kit_id: int, item_id: int):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(welcome_kit_id=welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!!"})
    
    welcome_kit_item_image = dao.select_welcome_kit_item_image(welcome_kit_id, item_id)
    
    if welcome_kit_item_image:
        return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit_item_image)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Welcome kit item not encountered"})
    
    
@router.post("/register/welcomekit-item")
async def register_welcome_kit(welcome_kit_id: int, item_name: str, item_image: UploadFile = File(...)):
    
    is_allowed_file = verify_is_allowed_file(item_image.filename)
    
    if not is_allowed_file:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail={"msg": "This format file is not permited!"})
    
    item_id = await dao.insert_welcome_kit(kit_item_name=item_name, kit_item_image=item_image)
    
    if not item_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been registered"})
    
    associate_item = dao.associate_item_with_kit(welcome_kit_id, item_id["id_item"])
    
    if associate_item:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been registered"})
  
        
@router.delete("/delete")
def delete_welcomekit(welcome_kit_id: int):
     
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(welcome_kit_id=welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!!"})
    
    
    welcome_kit_deleted = dao.delete_welcome_kit(welcome_kit_id)
    
    
    if welcome_kit_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The welcome kit has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR in WelcomeKit"})        
    
    
    
