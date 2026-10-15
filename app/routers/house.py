from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.repository.house_repository import HouseRepository
from app.service.house_service import HouseService
from app.schemas.house import HouseRequest, HouseResponse
from app.repository.user_repository import UserRepository


router = APIRouter(prefix="/houses", tags=["House"] )



async def get_house_service( db:AsyncSession=Depends(get_db) ):
  repo = HouseRepository(db)
  user_repo = UserRepository(db)
  return HouseService(repo=repo, user_repo=user_repo)


@router.get("/{house_id}", response_model=HouseResponse)
async def get_user_by_id( house_id:str, house_service=Depends(get_house_service) ):
  return await house_service.get_house_by_id(house_id)


@router.post("/", response_model=HouseResponse, status_code=status.HTTP_201_CREATED )
async def create_house( house_data:HouseRequest, house_service=Depends(get_house_service) ):
  return await house_service.create_house( house_data )


@router.get("/")
async def get_houses( house_service=Depends(get_house_service) ):
  return await house_service.get_all_houses()



# @router.post("/{house_id}/join")
# async def join_house():
#   pass

