
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.house import House
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError



class HouseRepository:

  def __init__(self, db:AsyncSession ):
    self.db = db

  async def get_by_id( self, house_id:str ) -> House | None:
    house = await self.db.execute( select(House).options(joinedload(House.creator)).where(House.id==house_id) )
    return house.scalar_one_or_none()

  async def get_by_joincode( self, join_code:str ) -> House | None :
    house = await self.db.execute( select(House).options(joinedload(House.creator)).where(House.join_code==join_code) )
    return house.scalar_one_or_none()


  async def create( self, house:House ) -> House:
    try:
      self.db.add( house )
      await self.db.flush()

      stmt = select(House).options( joinedload(House.creator) ).where( House.id==house.id )
      result = await self.db.execute( stmt )

      return result.scalar_one()

    except IntegrityError:
      await self.db.rollback()
      raise



  async def get_all( self ) -> list[House]:
    houses = await self.db.execute( select(House).options( joinedload(House.creator)) )
    return houses.scalars().all()

