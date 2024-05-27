from pydantic import BaseModel
from bson.objectid import ObjectId
from app.database import donor_collection
from typing import Any
"""
donor module
"""


class DonorBase(BaseModel):
    """ Base model for donor """
    name: str


class DonorCreate(DonorBase):
    """ Model for creating a donor """
    pass


class Donor(DonorBase):
    """ class to represent a donor """
    id: str
    user_id: str

    class Config:
        """ pydantic configuration for donor """
        from_attributes = True


def donor_helper(donor: Any) -> dict:
    """ helper fuction to transform donor document to dictionary """
    return {
        "id": str(donor["_id"]),
        "name": donor["name"],
        "user_id": donor["user_id"],
    }


async def create_donor(donor: DonorCreate, user_id: str) -> dict:
    """ function that creates a new donor"""
    donor_dict = donor.dict()
    donor_dict['user_id'] = user_id
    new_donor = await donor_collection.insert_one(donor_dict)
    return donor_helper(await donor_collection.find_one({"_id": new_donor.inserted_id}))
