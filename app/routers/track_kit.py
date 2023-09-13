from app.dao.dao_track_kit import insert_pack, select_pack, update_track, delivered_kit
from app.schemas.track_kit import TrackKitCreate, TrackKitEdit
from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/track_kit",
    tags=[
        "kit"
    ]
)


@router.get("/view")
def view_pack(employee_id: int):
    pack = select_pack(employee_id=employee_id)

    if pack:
        return JSONResponse(status_code=status.HTTP_200_OK, content=pack)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This employee doesn't have a welcome kit!"})

@router.post("/create")
def create_pack(create_track_kit: TrackKitCreate):
    create = insert_pack(employee_id=create_track_kit.employee_id, welcome_kit_id=create_track_kit.welcome_kit_id, tracking_code=create_track_kit.tracking_code, status=create_track_kit.status)

    if create:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This welcome kit track has been created!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit track can't be created!"})


@router.put("/edit")
def modify_track(edit_track_kit: TrackKitEdit):
    modify = update_track(tracking_code=edit_track_kit.tracking_code, status=edit_track_kit.status)

    if modify:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This tracking has been modified!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit can't be modified!"})

@router.put("/delivered_kit")
def modify_track(employee_id: int):
    modify = delivered_kit(employee_id=employee_id)

    if modify:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "This tracking has been delivered!"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This welcome kit can't be modified!"})