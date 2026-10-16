
from pydantic import BaseModel, ConfigDict
import uuid
from app.enums.HouseMembershipRole import HouseMembershipRole
from app.schemas.user import UserResponse
from app.schemas.house import HouseResponse
import datetime



class HouseMembershipRequest( BaseModel ):
  user_id:uuid.UUID
  house_id:uuid.UUID
  role: HouseMembershipRole


class HouseMembershipResponse( BaseModel ):
  id:int
  user_id:uuid.UUID
  house_id:uuid.UUID
  role:HouseMembershipRole
  user:UserResponse
  house:HouseResponse
  joined_at:datetime.datetime
  model_config=ConfigDict(from_attributes=True)

