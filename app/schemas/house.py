
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse
import uuid


class HouseRequest(BaseModel):
  name:str
  description:str
  currency:str | None = "INR"
  created_by:uuid.UUID


class HouseResponse(BaseModel):
  id:uuid.UUID
  name:str
  description:str
  join_code:str
  currency:str
  created_by:uuid.UUID
  creator:UserResponse
  model_config = ConfigDict(from_attributes=True)


