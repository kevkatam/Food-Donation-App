from pydantic import BaseModel
from bson.objectid import ObjectId
from app.database import recipient_collection
"""
recipient module
"""


class RecipientBase(BaseModel):
    """ base model for recipient """
    name: str


class RecipientCreate(RecipientBase):
    """ model for creating a recipient """
    pass


class Recipient(RecipientBase):
    """ class to represent a recipient """
    id: str
    user_id: str

    class Config:
        """pydantic configuration for recipient """
        from_attributes = True


def recipient_helper(recipient) -> dict:
    """Helper function to transform recipient document into dictionary"""
    return {
        "id": str(recipient["_id"]),
        "name": recipient["name"],
        "user_id": recipient["user_id"],
    }


async def create_recipient(recipient: RecipientCreate, user_id: str):
    """Create a new recipient"""
    recipient_dict = recipient.dict()
    recipient_dict['user_id'] = user_id
    new_recipient = await recipient_collection.insert_one(recipient_dict)
    return recipient_helper(await recipient_collection.find_one({"_id": new_recipient.inserted_id}))
