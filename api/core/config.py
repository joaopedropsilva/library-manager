from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str
    api_desc: str
    api_version: str

    database_url: str

    default_loan_term_in_days: int
    fine_amount_per_day: float
    max_active_loans_per_user: int

    model_config = {"env_file": ".env"}

settings = Settings()
