from app.dao import dao_employee
from app.schemas.employee import FeedBackEmployee
from fastapi import APIRouter


router = APIRouter(
    prefix="/employee",
    tags=[
        "employee"
    ]
    
                   )


@router.get("/")
def get_feedback_employee(employee_id : int ):
    dao_employee()
    return 



@router.post("/register")
def create_feedback_employee(feedback_employee: FeedBackEmployee):
    print(feedback_employee.employee_id)

@router.put("/update")
def update_feedback_employee(feedback_employee: FeedBackEmployee):
    dao_employee()
    return feedback_employee


