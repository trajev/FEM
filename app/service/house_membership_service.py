
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repository.house_membership_repository import HouseMembershipRepository
from app.schemas.house_membership import  HouseMembershipResponse
from app.repository.house_repository import HouseRepository
from app.models.house_membership import HouseMembership
import uuid

class HouseMembershipService:

  def __init__(self, repo:HouseMembershipRepository, house_repo:HouseRepository ):
    self.repo = repo
    self.house_repo = house_repo


  async def get_all_hm(self) -> list[HouseMembership]:
    return await self.repo.get_all()


  async def join_house( self, user_id:uuid.UUID, join_code:str ) -> HouseMembershipResponse:
    house = await self.house_repo.get_by_joincode( join_code )
    if house is None:
      raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"House not found with join code: {join_code}" )



    try:
      hm = HouseMembership( user_id=user_id, house_id=house.id )
      return await self.repo.create( hm )
    except IntegrityError as e:
      await self.repo.db.rollback()
      error_msg = str(e.orig).lower()

      # Check if they violated the 1-house-per-user rule
      if "house_memberships_user_id_key" in error_msg:
          raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already a member of a house. You must leave your current house before joining a new one." )

      raise


