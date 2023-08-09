from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.enterprise import router as router_enterprise
from app.routers.tool import router as router_tool
from app.routers.quiz import router as router_quiz
from app.routers.gamified_journey import router as router_gamified_journey




app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3306",
    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router_enterprise)
app.include_router(router=router_tool)
app.include_router(router=router_quiz)
app.include_router(router=router_gamified_journey)