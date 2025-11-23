from app.core.log import setup_logger


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

    from app.api.v1.routes import user
    from app.api.v1.routes import book
    from app.api.v1.routes import loan

    app = FastAPI(title="library-manager")

    logger.debug("Created FastAPI instance")

    app.include_router(user.router, prefix="/api/v1")
    app.include_router(book.router, prefix="/api/v1")
    app.include_router(loan.router, prefix="/api/v1")

    uvicorn.run("app.run:app", host="0.0.0.0", port=8000, reload=True)
