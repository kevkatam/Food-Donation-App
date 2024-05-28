from fastapi import FastAPI
from app.routes import donations, user, donor, recipient, reviews

app = FastAPI()

# routes from other modules
app.include_router(user.router)
app.include_router(donor.router)
app.include_router(donations.router)
app.include_router(recipient.router)
app.include_router(reviews.router)
