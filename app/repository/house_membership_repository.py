from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.house_membership import HouseMembership

class HouseMembershipRepository:

  def __init__(self, db:AsyncSession ):
    self.db = db


  async def create(self, data:HouseMembership ) -> HouseMembership :
    try:
      self.db.add( data )
      await self.db.commit()
      await self.db.refresh(data)
      return data
    except Exception:
      await self.db.rollback()
      raise


  async def get_by_id( self ):
    pass


  async def get_all( self ) -> list[HouseMembership]:
    hm_data = await self.db.execute( select(HouseMembership).options( joinedload(HouseMembership.user), joinedload(HouseMembership.house) ) )
    return hm_data.scalars().all()

  
