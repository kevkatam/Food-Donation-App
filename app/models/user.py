from pydantic import BaseModel
"""
user model
"""


class UserBase(BaseModel):
    """ base model for User """
    username: str


class UserCreate(UserBase):
    """ model for creating a user """
    password: str


class User(UserBase):
    """ class to represent a User """
    id: str

    class Config:
        """ pydantic configuration for user """
        from_attributes = True
