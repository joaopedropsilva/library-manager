from contextlib import asynccontextmanager
from api.core.log import setup_logger


def setup_api(*, log_level_override: str = ""):
    setup_logger(log_level_override)

    import logging
    logger = logging.getLogger(__name__)

    # Imports after logger setup to make
    # sure all loggers used on modules
    # use the configured logger
    from fastapi import FastAPI

    #from api.db.session import get_session
    from api.versions.v1.routes import user
    from api.versions.v1.routes import book
    from api.versions.v1.routes import loan


    @asynccontextmanager
    async def lifespan(app):
        logger.debug("Starting API dependencies")
        #get_session()
        yield
        logger.debug("Deactivating API dependencies")


    app = FastAPI(title="library-manager", lifespan=lifespan)

    logger.debug("Created FastAPI instance")

    app.include_router(user.router, prefix="/api/v1")
    app.include_router(book.router, prefix="/api/v1")
    app.include_router(loan.router, prefix="/api/v1")


    @app.get("/")
    async def root_route():
        return {"msg": "Hello from library-manager"}


    return app
