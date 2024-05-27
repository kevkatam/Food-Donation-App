from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.database import review_collection
from app.models.user import User

"""
review model
"""

class ReviewBase(BaseModel):
    """ base model for Review """
    title: str
    content: str
    rating: int

    class Config:
        """ pydantic configuration for review """
        arbitrary_types_allowed = True

class ReviewCreate(ReviewBase):
    """ model for creating a review """
    user_id: str = Field(..., alias="userId")

class Review(ReviewBase):
    """ class to represent a Review """
    id: str
    user_id: str

    class Config:
        """ pydantic configuration for review """
        from_attributes = True

def review_helper(review) -> dict:
    """ helper function to transform review document into dictionary """
    return {
        "id": str(review["_id"]),
        "title": review["title"],
        "content": review["content"],
        "rating": review["rating"],
        "user_id": str(review["user_id"]),
    }

async def create_review(review: ReviewCreate):
    """ creates a new review """
    review_dict = review.dict(by_alias=True)
    new_review = await review_collection.insert_one(review_dict)
    return review_helper(await review_collection.find_one({"_id": new_review.inserted_id}))

async def get_reviews_by_user_id(user_id: str):
    """ function that gets reviews by user id """
    reviews = await review_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)
    return [review_helper(review) for review in reviews]

