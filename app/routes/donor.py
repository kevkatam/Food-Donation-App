from fastapi import APIRouter, Depends, HTTPException
from app.models.donor import Donor, DonorCreate, create_donor
from app.routes.auth import get_current_user
from app.models.user import User


router = APIRouter()

@router.post("/donors/", response_model=Donor)
async def create_donor_endpoint(donor: DonorCreate, current_user: User = Depends(get_current_user)):
    """
    creates a new donor
    Args:
        donor: donor to data to be created
        current_user: logged-in user, obtained through dependency injection
    Returns:
        dict: a dictionary containing created donor's details
    """
    donor_id = await create_donor(donor, user_id=current_user["id"])
    return {"id": donor_id, "name": donor.name, "user_id": current_user["id"]}
