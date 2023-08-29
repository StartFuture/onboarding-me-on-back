from app.dao.dao_tools import verify_if_company_exists
from app.schemas.employee import FeedBackEmployee
from fastapi import APIRouter
from app.dao import dao_employee as dao
from fastapi import APIRouter,status, HTTPException
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/employee",
    tags=[
        "employee"
    ]
    
                   )


@router.get("/feedback")
def get_feedback_employee(company_id : int):

    feedback_exists = verify_if_company_exists(company_id)

    if not feedback_exists:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't exists"})

    feedback_list = dao.select_feedback_company(company_id = company_id )

    if feedback_list:
        return JSONResponse (status_code=status.HTTP_200_OK, content=feedback_list)
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "This company don't have feedbacks"})

@router.get("/score")
def get_final_score(employee_id: int):
    
    employee_exists = dao.verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    
    total_score = dao.get_total_score(employee_id)
    
    if total_score or total_score == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=total_score)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Employee score not encountered!"})   
    

@router.post("/register/score") 
def register_score(employee_id: int):

    employee_exists = dao.verify_employee_exists(employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})
    
    
    score_registered = dao.insert_employee_score(employee_id)
    
    if score_registered:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg":"The score has been registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Incorrect answer!"})

@router.post("/register/feedback")
def create_feedback_employee(feedback_employee: FeedBackEmployee):

    employee_exists = dao.verify_employee_exists(feedback_employee.employee_id)
    
    if not employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "This employee not exists!"})

    is_register = dao.insert_feedback(feedback_employee)

    if is_register:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})