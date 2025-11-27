from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    _postgres_host: str
    _postgres_port: int
    _postgres_user: int
    _postgres_db: str
    _postgres_password: str
    database_url: str

    model_config = {"env_file": ".env"}

settings = Settings()
