from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.models.donation import Donation, DonationCreate, create_donation, get_donations, get_donation_by_id
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/donations/", response_model=Donation)
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
    donation_data = await create_donation(donation)
    return donation_data
    """return {"id": donation_id, **donation.dict()}"""


@router.get("/donations/", response_model=List[Donation])
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


@router.get("/donations/{id}", response_model=Donation)
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


@router.put("/donations/{id}", response_model=Donation)
async def update_donation(id: str, donation: DonationCreate):
    """ updates a donation's information
    Args:
        id (str): The id of the donation to update
        donation (DonationCreate): The updated donation data
    Returns:
        Donation: The updated donation data
    """
    donation_data = await update_donation(id, donation)
    return donation_data


@router.delete("/donations/{id}")
async def delete_donation(id: str):
    """ deletes a donation by its ID
    Args:
        id (str): The id of the donation to delete
    Returns:
        dict: a dictionary containing a message indicating the deletion
    """
    await delete_donation(id)
    return {"message": "Donation deleted successfully"}
