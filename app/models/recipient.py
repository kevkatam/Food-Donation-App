from pydantic import BaseModel
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
