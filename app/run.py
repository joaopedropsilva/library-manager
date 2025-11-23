import uvicorn
from fastapi import FastAPI


app = FastAPI(title="btg-library")


def start_api():
    # configure logger here

    from app.api.v1.routes import user
    from app.api.v1.routes import book
    from app.api.v1.routes import loan

    app.include_router(user.router, prefix="/api/v1")
    app.include_router(book.router, prefix="/api/v1")
    app.include_router(loan.router, prefix="/api/v1")

    uvicorn.run("app.run:app", host="0.0.0.0", port=8000, reload=True)
