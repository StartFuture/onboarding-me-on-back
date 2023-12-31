from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.schemas.address import Address 
from app.dao import dao_address as dao
from app.auth import verify_token_employee_or_company, verify_token_employee, verify_token_company

router = APIRouter(
    prefix="/address",
    tags=[
        "address"
    ]
)


@router.get("/by-employee")
def get_address_by_employee(payload: dict = Depends(verify_token_employee)):

    address_exists = dao.verify_if_address_exists(employee_id=payload['sub'])
        
    if not address_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Address dont exists!"})

    address = dao.select_address(payload['sub'])
    
    if address:
        return JSONResponse(status_code=status.HTTP_200_OK, content=address)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    
    
@router.get("/by-company")
def get_address_by_company(employee_id: int, payload: dict = Depends(verify_token_company)):
     
    address_exists = dao.verify_if_address_exists(employee_id=employee_id)

    if not address_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Address dont exists!"})
    
    address = dao.select_address(employee_id)

    if address:
        return JSONResponse(status_code=status.HTTP_200_OK, content=address)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})


@router.post("/register")
def create_address(address: Address, payload: dict = Depends(verify_token_employee_or_company)):
    
    addresses = dao.verify_if_address_exists_by_house(company_id=payload['company'])
    
    for address_data in addresses:
        if address_data['num'] == address.num and address_data['street'] == address.street:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address already exists!"})
        
    
    address.zipcode = address.zipcode.replace('-', '')

    address_registered = dao.insert_address(address)
    
    if address_registered:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully created"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    
    
@router.put("/update")
def modify_address(address: Address, payload: dict = Depends(verify_token_employee_or_company)):
    
    addresses_list = []
    
    addresses = dao.return_company_addresses(payload['company'])
    
    for address_id in addresses:
        addresses_list.append(address_id['id'])
    
    if address.address_id not in addresses_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address does not exists!"})

    address.zipcode = address.zipcode.replace('-', '')
    
    address_updated = dao.update_address(address)
    
    if address_updated:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})

    
@router.delete("/delete")
def del_address(address_id: int, payload: dict = Depends(verify_token_company)):
    
    addresses_list = []
    
    addresses = dao.return_company_addresses(payload['company'])
    
    for address in addresses:
        addresses_list.append(address['id'])
        
    if address_id not in addresses_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Address does not exists!"})
    
    address_deleted = dao.delete_address(address_id)
    
    if address_deleted:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Successfully deleted"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Error in address"})
    