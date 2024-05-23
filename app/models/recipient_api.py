from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

recipients = {
    1: {
        "name": "kyalo",
        "age": "10",
        "id": 1
    },
    2: {
        "name": "kamau",
        "age": "20",
        "id": 2
    },
    3: {
        "name": "kamene",
        "age": "30",
        "id": 3
    }
}


class Recipient(BaseModel):
    name: str
    age: int
    id: int

class UpdateRecipient(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    id: Optional[int] = None


@app.get("/")
def index():
    return {"name": "First Data"}


"""path parameters"""


@app.get("/get-recipient/{recipient_id}")
def get_recipient(recipient_id: int = Path(..., description="The ID of the recipient you want to view", gt=0)):
    return recipients.get(recipient_id, {"Data": "Not Found"})


"""query parameters"""


@app.get("/get-by-name")
def get_recipient(*, recipient_id: int, name: Optional[str] = None, test: int):
    for recipient_id in recipients:
        if recipients[recipient_id]["name"] == name:
            return recipients[recipient_id]
    return {"Data": "Not Found"}


"""request body"""


@app.post("/create-recipient/{recipient_id}")
def create_recipient(recipient_id: int, recipient: Recipient):
    if recipient_id in recipients:
        return {"Error": "Recipient ID already exists"}
    recipients[recipient_id] = recipient
    return recipients[recipient_id]


@app.put("/update-recipient/{recipient_id}")
def update_recipient(recipient_id: int, recipient: Recipient):
    if recipient_id not in recipients:
        return {"Error": "Recipient ID does not exist"}

    if recipient.name is not None:
        recipients[recipient_id]["name"] = recipient.name

    if recipient.age is not None:
        recipients[recipient_id]["age"] = recipient.age

    if recipient.id is not None:
        recipients[recipient_id]["id"] = recipient.id
    
    recipients[recipient_id] = recipient
    return recipients[recipient_id]


@app.delete("/delete-recipient/{recipient_id}")
def delete_recipient(recipient_id: int):
    if recipient_id not in recipients:
        return {"Error": "Recipient ID does not exist"}
    del recipients[recipient_id]
    return {"Message": "Recipient deleted successfully"}

