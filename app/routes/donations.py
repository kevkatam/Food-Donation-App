from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.models.donation import Donation, DonationBase, DonationCreate, create_donation, get_donations, get_donation_by_id, delete_donation, update_donation
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
async def update_donation_endpoint(id: str, donation_data: DonationBase, current_user = Depends(get_current_user)):
    """ updates a donation by its ID
    Args:
        id: donation id to update
        donation_data: updated donation data
    Returns:
        Donation: updated donation
    Raises:
        HTTPException: if donation with specified id is not found
    """
    updated_donation = await update_donation(id, donation_data)
    if updated_donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return updated_donation


@router.get("/donors/{donor_id}/donations/", response_model=List[Donation])
async def get_donations_by_donor(donor_id: str, skip: int = 0, limit: int = 10):
    """ gets a list of donations by donor ID with pagination
    Args:
        donor_id: donor id whose donation to retrieve
        skip: the number of donations to skip, default 0
        limit: max number of donations to return default 10
    Return:
        List[Donation]: a list of donations made by the specified donor
    """
    donations = await get_donations_by_donor_id(donor_id, skip=skip, limit=limit)
    if not donations:
        raise HTTPException(status_code=404, detail="No donations found for this donor")
    return donations


@router.delete("/donations/{id}", response_model=dict)
async def delete_donation_endpoint(id: str, current_user: User = Depends(get_current_user)):
    """ deletes a donation by its ID
    Args:
        id: The id of the donation to delete
    Returns:
        dict: message indicating result of delete operation
    """
    deleted = await delete_donation(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Donation not found")
    return {"message": "Donation deleted successfully"}
