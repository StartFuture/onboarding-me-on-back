from fastapi import APIRouter,status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao import dao_track_kit as dao
from app.dao.dao_welcomekit import verify_if_welcome_kit_exists
from app.schemas.track_kit import TrackKitCreate
from app.auth import verify_token_company, verify_token_employee_or_company, verify_token_employee


router = APIRouter(
    prefix="/track_kit",
    tags=[
        "tracking"
    ]
)


@router.get("/")
def view_pack(payload: dict = Depends(verify_token_employee)):
    
    pack = dao.select_pack(employee_id=payload['sub'])

    if pack:
        return JSONResponse(status_code=status.HTTP_200_OK, content=pack)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee doesn't have a welcome kit!"})


@router.post("/register")
def create_pack(create_track_kit: TrackKitCreate, payload: dict = Depends(verify_token_company)):
    
    welcome_kit_exists = verify_if_welcome_kit_exists(welcome_kit_id=create_track_kit.welcome_kit_id)
    
    if not welcome_kit_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This welcome kit doesn't exists!"})

    create = dao.insert_pack(employee_id=create_track_kit.employee_id, welcome_kit_id=create_track_kit.welcome_kit_id)

    if create:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This welcome kit track has been created!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit track can't be created!"})


@router.put("/update/status-sended")
def modify_status_to_sended(tracking_id: int, tracking_code: str, payload: dict = Depends(verify_token_company)):
    
    tracking_exists = dao.verify_if_tracking_exists(tracking_id)
    
    if not tracking_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This tracking doesn't exists!"})
    
    modify = dao.update_track_status_to_sended(tracking_id=tracking_id, tracking_code=tracking_code)

    if modify:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This tracking has been modified!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit can't be modified!"})
    
    
    
@router.put("/update/status-delivered")
def modify_status_to_delivered(tracking_id: int, payload: dict = Depends(verify_token_employee_or_company)):
    
    tracking_exists = dao.verify_if_tracking_exists(tracking_id)
    
    if not tracking_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This tracking doesn't exists!"})
    
    modify = dao.update_track_status_to_delivered(tracking_id=tracking_id)

    if modify:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This tracking has been modified!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit can't be modified!"})