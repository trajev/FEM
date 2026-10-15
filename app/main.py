from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.house import router as house_router

app = FastAPI()


app.include_router( user_router )
app.include_router( house_router )
