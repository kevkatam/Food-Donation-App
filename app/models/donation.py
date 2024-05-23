from pydantic import BaseModel
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
