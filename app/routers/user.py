from fastapi import APIRouter, Depends, Path, status
from app.db.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRequest, UserResponse
from app.service.user_service import UserService

router = APIRouter( prefix="/users" )


def get_user_service( db:AsyncSession=Depends(get_db) ) -> UserService :
  return UserService(db)

@router.get("/", response_model=list[UserResponse])
async def get_users( service:UserService=Depends(get_user_service) ) :
  return await service.get_all_users()

@router.post("/",response_model=UserResponse, status_code=status.HTTP_201_CREATED )
async def create_user( user_data:UserRequest, service:UserService=Depends(get_user_service) ):
  return await service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse )
async def get_user_by_id( user_id:int=Path(gt=0), service:UserService=Depends(get_user_service) ):
  return await service.get_user_by_id(user_id)

