from fastapi import FastAPI
from .models import Recipient, RecipientCreate


app = FastAPI()

@app.post("/recipients/", response_model=Recipient)
async def create_recipient_endpoint(recipient: RecipientCreate, current_user: User = 
