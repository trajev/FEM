from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.repository.house_repository import HouseRepository
from app.service.house_service import HouseService
from app.schemas.house import HouseRequest, HouseResponse
from app.repository.user_repository import UserRepository
from app.repository.house_membership_repository import HouseMembershipRepository
from app.service.house_membership_service import HouseMembershipService
import uuid


router = APIRouter(prefix="/houses" )



async def get_house_service( db:AsyncSession=Depends(get_db) ):
  repo = HouseRepository(db)
  user_repo = UserRepository(db)
  hm_repo = HouseMembershipRepository(db)
  return HouseService(repo=repo, user_repo=user_repo, hm_repo=hm_repo)


async def get_hm_service( db:AsyncSession=Depends(get_db) ):
  repo = HouseMembershipRepository(db)
  house_repo = HouseRepository(db)
  return HouseMembershipService( repo=repo, house_repo=house_repo )



@router.get("/{house_id}", response_model=HouseResponse)
async def get_user_by_id( house_id:str, house_service=Depends(get_house_service) ):
  return await house_service.get_house_by_id(house_id)


@router.post("/", response_model=HouseResponse, status_code=status.HTTP_201_CREATED )
async def create_house( house_data:HouseRequest, house_service=Depends(get_house_service) ):
  return await house_service.create_house( house_data )


@router.get("/")
async def get_houses( house_service=Depends(get_house_service) ):
  return await house_service.get_all_houses()


@router.post("/join" )
async def join_house( user_id:uuid.UUID, join_code:str, hm_service=Depends(get_hm_service) ):
  return await hm_service.join_house( user_id, join_code )
