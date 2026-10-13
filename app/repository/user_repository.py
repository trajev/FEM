from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserRequest

class UserRepository:

  def __init__( self, db:AsyncSession ):
    self.db = db

  async def get_by_email(self, emailId:str ) -> User:
    user = await self.db.execute( select(User).where(User.email==emailId) )
    return user.scalar_one_or_none()

  async def get_all(self) -> list[User]:
    result = await self.db.execute( select(User) )
    return result.scalars().all()

  async def create(self, user_data:UserRequest ) -> User :
    user = User( name=user_data.name, email=user_data.email )
    self.db.add(user)
    await self.db.flush()
    await self.db.refresh(user)
    return user

  async def get_by_id( self, user_id:int ) -> User:
    user = await self.db.execute( select(User).where(User.id==user_id) )
    return user.scalar_one_or_none()