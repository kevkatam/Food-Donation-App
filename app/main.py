from fastapi import FastAPI
from app.routes import donations, user

app = FastAPI()

# routes from other modules
app.include_router(user.router)
app.include_router(donations.router)
