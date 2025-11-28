from api.core.log import setup_logger
from api.db.models.models import *


def setup_api(*, log_level_override: str = ""):
    setup_logger(log_level_override)

    import logging
    logger = logging.getLogger(__name__)

    # Imports after logger setup to make
    # sure all loggers used on modules
    # use the configured logger
    from fastapi import FastAPI

    from api.versions.v1.routes import user
    from api.versions.v1.routes import book
    from api.versions.v1.routes import loan

    app = FastAPI(title="library-manager")

    logger.debug("Created FastAPI instance")

    app.include_router(user.router, prefix="/api/v1", tags=["Users"])
    app.include_router(book.router, prefix="/api/v1", tags=["Books"])
    app.include_router(loan.router, prefix="/api/v1", tags=["Loans"])


    @app.get("/")
    async def root_route():
        return {"msg": "Hello from library-manager"}


    return app
