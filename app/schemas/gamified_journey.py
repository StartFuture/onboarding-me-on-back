from pydantic import BaseModel, Field, constr


class GamifiedJourney(BaseModel):
    welcome_video_link: str
    company_id: int
    