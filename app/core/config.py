from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DATABASE_URL:str
  PORT:int=8000
  DEBUG:bool=False
  APP_NAME:str="Family Expense Manager"
  model_config = SettingsConfigDict( env_file=".env" )


settings = Settings()

