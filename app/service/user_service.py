from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserRequest
from fastapi import HTTPException, status
from app.repository.user_repository import UserRepository

class UserService:

    def __init__(self, db:AsyncSession ):
        self.repo = UserRepository(db)

    async def get_all_users(self ) -> list[User]:
        return await self.repo.get_all()

    async def create_user(self, user_data:UserRequest ) -> User:
        existing_user = await self.repo.get_by_email( user_data.email )
        if existing_user:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="User already exist with this Email ID")
        return await self.repo.create( user_data )

    async def get_user_by_id( self, user_id:int ) -> User:
        user = await self.repo.get_by_id( user_id )
        if not user:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found with id {user_id}" )
        return user

