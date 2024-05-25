from user import app
from fastapi import Depends, HTTPException
from typing import List
from app.models.donation import Donation, DonationCreate, create_donation, get_donations, get_donation_by_id
from app.auth import get_current_user
from app.models.user import User


@app.post("/donations/", response_model=Donation)
async def create_donation_endpoint(donation: DonationCreate, current_user: User = Depends(get_current_user)):
    """ creates a new donation
    Args:
        donation (DonationCreate): donation data to be created
        current_user (User): current logged-in user, obtained through
                             dependenxy injection
    Return:
        dict: A dictionary conating the created donation's details,
              and donation id
    """
    donation_id = await create_donation(donation)
    return {"id": donation_id, **donation.dict()}


@app.get("/donations/", response_model=List[Donation])
async def gett_donations(skip: int = 0, limit: int = 10):
    """ gets a list of donations with pagination
    Args:
        skip (int): the number of donations to skip. Default to 0
        limit (int): maximum number of donation to return. Default 10
    Return:
        List[Donation]: a list of donations within the specified range
    """
    donations = await get_donations(skip=skip, limit=limit)
    return donations


@app.get("/donations/{id}", response_model=Donation)
async def get_donation(id: str):
    """ gets a single donation by its ID
    Args:
        id (str): The id of the donation to retrieve
    Returns:
        Donation: The donation with specified ID
    Raises:
        HTTPException: if the donation with the specified ID is not found
    """
    donation = await get_donation_by_id(id)
    if donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation
