from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse

from app.dao import dao_welcomekit as dao
from app.dao.dao_employee import verify_employee_exists
from app.schemas.tracking_code import TrackingCode

router = APIRouter(prefix="/welcomekit",     
                    tags=["welcomekit"] 
                    )   

@router.get("/tracking-code")
def get_tracking_code(employee_id: int):

    tracking_code = dao.select_tracking(employee_id)

    if tracking_code:
        return JSONResponse (status_code=status.HTTP_200_OK, content=tracking_code)
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This tracking don't exist"})

@router.post("/register/tracking")
def register_tracking(employee_id, welcome_kit_id: int):
    
    registered_tracking = dao.insert_tracking(employee_id,welcome_kit_id)

    if registered_tracking:
        return JSONResponse (status_code=status.HTTP_200_OK, content={"msg": "The tracking register"})
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The tracking don't register"})


@router.put("/update/tracking")
def modify_tracking(tracking_code: TrackingCode):
    
    employee_exists = verify_employee_exists(tracking_code.employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})

    modified_trancking = dao.update_tracking(tracking_code)

    if modified_trancking:
        return JSONResponse (status_code=status.HTTP_200_OK, content={"msg": "The tracking is modified"})
    else:
        raise HTTPException (status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR"})
    
@router.put("/update/status")
def modify_status(employee_id: int ):
    
    employee_exists = verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    modify_status = dao.update_tracking_status_delivered(employee_id)

    if modify_status:
        return JSONResponse (status_code=status.HTTP_200_OK, content={"msg": "The status is modify"})
    else:
        raise HTTPException (status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR"})
    
    