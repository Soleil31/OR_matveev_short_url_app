from fastapi import FastAPI

from routers.urls import router as urls_router
from database.connect import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/")

app.include_router(urls_router)
