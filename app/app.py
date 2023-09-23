from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.company import router as router_company
from app.routers.tool import router as router_tool
from app.routers.quiz import router as router_quiz
from app.routers.employee import router as router_employee
from app.routers.gamified_journey import router as router_gamified_journey
from app.routers.welcome_kit import router as router_welcome_kit
from app.routers.track_kit import router as track_kit
from app.routers.medal import router as router_medal
from app.routers.authentication import router as router_login
from app.routers.password_edit import router as router_password_edit
from app.routers.address import router as router_address


app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:3001/",
    "http://localhost:3000/",
    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router_login)
app.include_router(router=router_password_edit)
app.include_router(router=router_company)
app.include_router(router=router_gamified_journey)
app.include_router(router=router_medal)
app.include_router(router=router_tool)
app.include_router(router=router_quiz)
app.include_router(router=router_employee)
app.include_router(router=router_address)
app.include_router(router=track_kit)
app.include_router(router=router_welcome_kit)
