from pydantic import BaseModel, Field
from typing import Optional

feedback_type_pattern = r"gamefiedjorney|welcomekit"

class FeedBackEmployee(BaseModel):
    employee_id: Optional[int] = None
    grade: int 
    message: Optional[str] = None
    feedback_type: str = Field(pattern=feedback_type_pattern)
