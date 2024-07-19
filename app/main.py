from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables defined in the models
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application and include the router from post and user files
app = FastAPI()

# Define the domains that can talk to the API (send requests). You can define ["*"] as a wildcard to be accessed from any website
origins = ["*"]

# Define the CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing the different operations defined in router folders
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# PATHS OPERATIONS ARE ON THE ROUTERS FOLDER
# The welcome page, as a test only
@app.get("/")
def root():
    return {'message': 'Hi there, welcome to the post blog'}