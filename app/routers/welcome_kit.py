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
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(employee_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit dont exists!"})
    
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
    
    
    
    