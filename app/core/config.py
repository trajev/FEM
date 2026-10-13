from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DATABASE_URL:str
  PORT:int=8000
  DEBUG:bool=False
  model_config = SettingsConfigDict( env_file=".env" )


settings = Settings()

