from fastapi import FastAPI
from . import models
from .database import engine
from .routers import entry, user, auth, post
from mangum import Mangum

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

handler_function = Mangum(app)

app.include_router(user.router)
app.include_router(entry.router)
app.include_router(auth.router)
app.include_router(post.router)

@app.get("/")
def homepage():
    return "Welcome to Paddy"