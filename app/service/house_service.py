from app.repository.house_repository import HouseRepository
from app.models.house import House
from fastapi import HTTPException, status
from app.schemas.house import HouseRequest, HouseResponse
from app.repository.user_repository import UserRepository
from app.utils.helper import generate_join_code


class HouseService:

  def __init__(self, repo:HouseRepository, user_repo:UserRepository ):
    self.repo = repo
    self.user_repo = user_repo


  async def get_house_by_id( self, house_id:str ) -> House | None :
    house = await self.repo.get_by_id( house_id )
    if house is None:
      raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"House not found with id {house_id}" )
    return house



  async def create_house( self, house_data:HouseRequest ) -> HouseResponse:

    user = await self.user_repo.get_by_id(house_data.created_by)

    if not user:
      raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="User not found. Cannot create house." )

    join_code = generate_join_code()
    new_house = House( **house_data.model_dump(), join_code=join_code  )
    return await self.repo.create( new_house )



  async def get_all_houses( self ) -> list[HouseResponse]:
    return await self.repo.get_all()