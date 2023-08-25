from app.dao import dao_employee as dao
from app.dao.dao_tools import verify_if_company_exists
from app.schemas.employee import FeedBackEmployee
from fastapi import APIRouter, status, HTTPException
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
    


@router.post("/register/feedback")
def create_feedback_employee(feedback_employee: FeedBackEmployee):
    is_register = dao.insert_feedback(feedback_employee)
    if is_register:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Successfully registered!"})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "ERROR!"})


