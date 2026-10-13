from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequest(BaseModel):
  name:str = Field( ..., min_length=1, max_length=50 )
  email:EmailStr

class UserResponse(BaseModel):
  id:int
  name:str
  email:str
  model_config = ConfigDict( from_attributes=True )
