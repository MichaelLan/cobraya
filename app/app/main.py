import uvicorn
from fastapi import FastAPI
from app.app.api.api_v1.api import api_router
from app.app.core.config import settings

from app.app.db.base_class import Base
from app.app.db.session import engine

# TODO: Create the tables and migrations with alembic
#  delete this and create the configuration with alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.1.0',
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redocs",
    debug=settings.DEGUG,
)


app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT,
                reload=True, debug=settings.DEGUG, workers=1)
