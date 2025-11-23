from contextlib import asynccontextmanager
from api.core.log import setup_logger


app = None


def start_api():
    setup_logger()

    import logging
    logger = logging.getLogger(__name__)

    # Imports after logger setup to make
    # sure all loggers used on modules
    # use the configured logger
    import uvicorn
    from fastapi import FastAPI

    from api.versions.v1.routes import user
    from api.versions.v1.routes import book
    from api.versions.v1.routes import loan


    @asynccontextmanager
    async def lifespan(app):
        logger.debug("Starting API dependencies")
        yield
        logger.debug("Deactivating API dependencies")


    app = FastAPI(title="library-manager", lifespan=lifespan)

    logger.debug("Created FastAPI instance")

    app.include_router(user.router, prefix="/api/v1")
    app.include_router(book.router, prefix="/api/v1")
    app.include_router(loan.router, prefix="/api/v1")

    uvicorn.run(app, host="0.0.0.0", port=8000)
