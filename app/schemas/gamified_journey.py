from pydantic import BaseModel


class GamifiedJourney(BaseModel):
    welcome_video_link: str
    