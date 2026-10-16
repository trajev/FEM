from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.house import router as house_router
from app.routers.house_membership import router as hm_router
from app.core.config import settings

app = FastAPI( title=settings.APP_NAME )


app.include_router( user_router, tags=["User"] )
app.include_router( house_router, tags=["House"] )
app.include_router( hm_router, tags=["House Membership"])
