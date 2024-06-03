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


class DonorUpdate(DonorBase):
    """ Model for updating a donor """
    pass


class Donor(DonorBase):
    """ class to represent a donor """
    id: str
    user_id: str

    class Config:
        """ pydantic configuration for donor """
        from_attributes = True


def donor_helper(donor: Any) -> dict:
    """ helper function to transform donor document to dictionary """
    return {
        "id": str(donor["_id"]),
        "name": donor["name"],
        "user_id": donor["user_id"],
    }


async def create_donor(donor: DonorCreate, user_id: str) -> dict:
    """ function that creates a new donor """
    donor_dict = donor.dict()
    donor_dict['user_id'] = user_id
    new_donor = await donor_collection.insert_one(donor_dict)
    return donor_helper(await donor_collection.find_one({"_id": new_donor.inserted_id}))


async def get_donor_by_id(donor_id: str) -> dict:
    """ function that gets a donor by ID """
    donor = await donor_collection.find_one({"_id": ObjectId(donor_id)})
    if donor:
        return donor_helper(donor)
    return None


async def get_donor_by_user_id(user_id: str) -> list:
    """ function that gets donors by user ID """
    donors = await donor_collection.find({"user_id": user_id}).to_list(length=None)
    return [donor_helper(donor) for donor in donors]


async def update_donor(donor_id: str, donor_data: DonorUpdate) -> dict:
    """ function to update a donor's information """
    donor = await donor_collection.find_one({"_id": ObjectId(donor_id)})
    if donor:
        await donor_collection.update_one({"_id": ObjectId(donor_id)}, {"$set": donor_data.dict()})
        return await get_donor_by_id(donor_id)
    return None


async def delete_donor(donor_id: str) -> bool:
    """ function to delete a donor by ID """
    donor = await donor_collection.find_one({"_id": ObjectId(donor_id)})
    if donor:
        await donor_collection.delete_one({"_id": ObjectId(donor_id)})
        return True
    return False
