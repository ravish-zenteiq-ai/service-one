from fastapi import FastAPI

from app.db.base import Base, create_engine, SessionLocal, engine

import app.models.model as model

from app.routes import (
    post,
    user,
    auth
)
from app.core.config import settings



model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return{"message": "This is root folder"}

