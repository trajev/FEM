from fastapi import APIRouter, Depends
from app.service.house_membership_service import HouseMembershipService
from app.db.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.house_membership import HouseMembershipRequest, HouseMembershipResponse
from app.repository.house_membership_repository import HouseMembershipRepository
from app.repository.house_repository import HouseRepository


router = APIRouter(prefix="/house_membership")


async def get_hm_service( db:AsyncSession=Depends(get_db) ):
  repo = HouseMembershipRepository(db)
  house_repo = HouseRepository( db )
  return HouseMembershipService(repo=repo, house_repo=house_repo )


@router.get("/", response_model=list[HouseMembershipResponse])
async def get_all_hm( hm_service:HouseMembershipService=Depends(get_hm_service) ):
  return await hm_service.get_all_hm()

