from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao import dao_welcomekit as dao
from app.auth import verify_token_employee, verify_token_company


router = APIRouter(
    prefix="/welcomekit",
    tags=[
        "welcomekit"
    ]
)


@router.get("/welcomekit")
def get_welcome_kit_employee(payload: dict = Depends(verify_token_employee)):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(employee_id=payload['sub'])
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!"})
    
    welcome_kit= dao.select_welcome_kit(employee_id=payload['sub'])
    
    if not welcome_kit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "welcome kit not found!"})
  
    return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit)
 
    
@router.get("/welcomekit-item")    
def get_welcome_kit_item_employee(payload: dict = Depends(verify_token_employee)):
    
    welcome_kit_item= dao.select_welcome_kit_item(employee_id=payload['sub'])
    
    if not welcome_kit_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Welcome kit item not found"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit_item)


@router.get("/welcomekit/company")
def get_welcome_kit_company(payload: dict = Depends(verify_token_company)):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(company_id=payload['sub'])
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!"})
    
    welcome_kit= dao.select_welcome_kit(company_id=payload['sub'])
    
    if not welcome_kit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "welcome kit not found!"})
  
    return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit)
 
    
@router.get("/welcomekit-item/company")    
def get_welcome_kit_item_company(payload: dict = Depends(verify_token_company)):
    
    welcome_kit_item= dao.select_welcome_kit_item(company_id=payload['sub'])
    
    if not welcome_kit_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Welcome kit item not found"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=welcome_kit_item)


@router.post("/register/welcomekit")
def register_welcome_kit(name: str, image: str, employee_id: int, payload: dict = Depends(verify_token_company)):
    
    welcome_kit_registered = dao.insert_welcome_kit(welcome_kit_name=name, welcome_kit_image=image, employee_id=employee_id)
    
    if welcome_kit_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit has not been registered"})


@router.post("/register/welcomekit-item")
def register_welcome_kit_item(welcome_kit_id: int, item_name: str, item_image: str, payload: dict = Depends(verify_token_company)):
    
    item_id = dao.insert_welcome_kit(kit_item_name=item_name, kit_item_image=item_image)
    
    if not item_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been registered"})
    
    associate_item = dao.associate_item_with_kit(welcome_kit_id, item_id["id_item"])
    
    if associate_item:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been registered"})
  
        
@router.delete("/delete")
def delete_welcomekit(welcome_kit_id: int, payload: dict = Depends(verify_token_company)):
     
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(welcome_kit_id=welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!!"})
    
    welcome_kit_deleted = dao.delete_welcome_kit(welcome_kit_id)
    
    if welcome_kit_deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The welcome kit has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR in WelcomeKit"})        
    
    
@router.delete("/delete/item")
def delete_welcomekit_item(welcome_kit_id: int, item_id: int, payload: dict = Depends(verify_token_company)):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(welcome_kit_id=welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!!"})
    
    item_exists = dao.verify_if_welcome_kit_have_this_item(welcome_kit_id, item_id)
    
    if not item_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit dont have this item!"})
    
    list_item_id = [item_id]
    
    deleted_associate = dao.delete_associate_welcome_kit_items(id_list=list_item_id)
    
    if not deleted_associate:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been deleted"})
        
    deleted_item = dao.delete_all_welcome_kit_items(id_list=list_item_id)
    
    if deleted_item:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The welcome kit item has been deleted!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR in WelcomeKit"})      


@router.put("/update")
def modify_welcome_kit(welcome_kit_id: int, welcome_kit_name: str, image: str, payload: dict = Depends(verify_token_company)):
    
    welcome_kit_exists = dao.verify_if_welcome_kit_exists(welcome_kit_id=welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit does not exists!!"})
    
    welcome_kit_modified = dao.update_welcome_kit(welcome_kit_id, welcome_kit_name, image)
    
    if welcome_kit_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully updated!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit has not been updated"})
        

@router.put("/update/welcome-kit-item")
def modify_welcome_kit_item(kit_item_id: int, kit_item_name: str, image: str, payload: dict = Depends(verify_token_company)):

    welcome_kit_item_exists = dao.verify_if_welcome_kit_item_exists(kit_item_id)
    
    if not welcome_kit_item_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit item does not exists!!"})

    welcome_kit_item_modified = dao.update_welcome_kit_item(kit_item_id, kit_item_name, image)
    
    if welcome_kit_item_modified:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully updated!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The welcome kit item has not been updated"})