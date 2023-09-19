from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.address import Address 
from app.dao import dao_address as dao

router = APIRouter(
    prefix="/address",
    tags=[
        "address"
    ]
)


@router.get("/")
def get_address(address_id: int):
    
    address_exists = dao.verify_if_address_exists(address_id)
    
    if not address_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Address dont exists!"})
    
    address = dao.select_address(address_id)
    
    if address:
        return JSONResponse(status_code=status.HTTP_200_OK, content=address)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    

@router.post("/register")
def create_address(address: Address):
    
    address_exists = dao.verify_if_address_exists_by_house(address.num, address.street)
    
    if address_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address already exists!"})
    
    address.zipcode = address.zipcode.replace('-', '')

    address_registered = dao.insert_address(address)
    
    if address_registered:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully created"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    
    
@router.put("/update")
def modify_address(address: Address):
    
    address_exists = dao.verify_if_address_exists_by_id(address.address_id)
    
    if not address_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address does not exists!"})

    address.zipcode = address.zipcode.replace('-', '')
    
    address_updated = dao.update_address(address)
    
    if address_updated:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})

    
@router.delete("/delete")
def del_address(address_id: int):
    
    address_exists = dao.verify_if_address_exists_by_id(address_id)
    
    if not address_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address does not exists!"})
    
    address_deleted = dao.delete_address(address_id)
    
    if address_deleted:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully deleted"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    