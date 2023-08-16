from app.dao import dao_employee as dao


from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/employee",
    tags=[
        "employee"
    ]
        )


@router.get("/{employee_id}")
def get_final_score(employee_id: int):
    
    employee_exists = dao.verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    
    total_score = dao.get_total_score(employee_id)
    
    if total_score or total_score == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=total_score)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Employee score not encountered!"})   
    
    

@router.post("/register") 
def register_score(employee_id: int):

    employee_exists = dao.verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    
    score_registered = dao.insert_employee_score(employee_id)
    
    if score_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The score has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Incorrect answer!"})