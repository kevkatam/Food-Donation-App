from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.reviews import Review, ReviewCreate, create_review, get_reviews_by_user_id
from app.models.user import get_user_by_username

router = APIRouter()

@router.post("/reviews/", response_model=Review)
async def register_review(review: ReviewCreate):
    """ this endpoint allows users to create a review
    Request Body:
        title: title of the review
        content: content of the review
        rating: rating of the review
        userId: id of the user creating the review
    """
    user = await get_user_by_username(review.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    review_id = await create_review(review)
    return {
        "id": review_id,
        "title": review.title,
        "content": review.content,
        "rating": review.rating,
        "user_id": review.user_id
    }

@router.get("/reviews/user/{user_id}", response_model=List[Review])
async def get_user_reviews(user_id: str):
    """ this endpoint allows users to fetch reviews by user id
    Path Parameter:
        user_id: id of the user
    """
    reviews = await get_reviews_by_user_id(user_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this user")
    return reviews
