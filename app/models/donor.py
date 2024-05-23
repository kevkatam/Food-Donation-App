from pydantic import BaseModel
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
