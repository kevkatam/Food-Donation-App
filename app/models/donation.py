from pydantic import BaseModel
from bson.objectid import ObjectId
from app.database import donation_collection

"""
donation module
"""


class DonationBase(BaseModel):
    """ class for donation model """
    food_item: str
    quantity: int


class DonationCreate(DonationBase):
    """ model for creating a donation """
    donor_id: str
    recipient_id: str


class Donation(DonationBase):
    """ class to represent a donation """
    id: str
    donor_id: str
    recipient_id: str

    class Config:
        """ pydantic configuration for donation """
        from_attributes = True


def donation_helper(donation) -> dict:
    """ helper function to transform donation document into dictionary """
    return {
        "id": str(donation["_id"]),
        "food_item": donation["food_item"],
        "quantity": donation["quantity"],
        "donor_id": donation["donor_id"],
        "recipient_id": donation["recipient_id"],
    }


async def create_donation(donation: DonationCreate):
    """ function that creates a new donation """
    donation_dict = donation.dict()
    new_donation = await donation_collection.insert_one(donation_dict)
    return donation_helper(await donation_collection.find_one({"_id": new_donation.inserted_id}))


async def get_donations(skip: int = 0, limit: int = 10):
    """ function that gets a list of donations """
    donations = await donation_collection.find().skip(skip).limit(limit).to_list(length=limit)
    return [donation_helper(donation) for donation in donations]


async def get_donation_by_id(id: str):
    """ function that gets donation by its id """
    donation = await donation_collection.find_one({"_id": ObjectId(id)})
    if donation:
        return donation_helper(donation)


async def delete_donation(id: str):
    """ function that deletes a donation by its id """
    delete_result = await donation_collection.delete_one({"_id": ObjectId(id)})
    return delete_result.deleted_count > 0


async def update_donation(id: str, donation_data: DonationBase):
    """ function that updates donation data """
    updated_data = donation_data.dict(exclude_unset=True)
    update_result = await donation_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    if update_result.modified_count > 0:
        return await get_donation_by_id(id)
    return None
