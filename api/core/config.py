from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    api_title: str
    api_desc: str
    api_version: str

    model_config = {"env_file": ".env"}

settings = Settings()
