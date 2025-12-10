from api.core.config import settings 


class UserMaxLoansExceededException(Exception):
    def __init__(self):
        super().__init__(f"User already exceeded max active loans of {settings.max_active_loans_per_user}")
