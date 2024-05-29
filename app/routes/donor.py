from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.donor import Donor, DonorCreate, DonorUpdate, create_donor, get_donor_by_id, get_donor_by_user_id, update_donor, delete_donor
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
    donor_data = await create_donor(donor, user_id=current_user["id"])
    return donor_data

@router.get("/donors/{donor_id}", response_model=Donor)
async def get_donor(donor_id: str, current_user: User = Depends(get_current_user)):
    """
    fetches a donor by ID
    Args:
        donor_id: ID of the donor
        current_user: logged-in user, obtained through dependency injection
    Returns:
        dict: a dictionary containing the donor's details
    """
    donor = await get_donor_by_id(donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    if donor["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this donor")
    return donor

@router.get("/donors/user/{user_id}", response_model=List[Donor])
async def get_donors_by_user(user_id: str, current_user: User = Depends(get_current_user)):
    """
    fetches all donors by user ID
    Args:
        user_id: ID of the user
        current_user: logged-in user, obtained through dependency injection
    Returns:
        list: a list of dictionaries containing the donors' details
    """
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access these donors")
    donors = await get_donor_by_user_id(user_id)
    if not donors:
        raise HTTPException(status_code=404, detail="No donors found for this user")
    return donors

@router.put("/donors/{donor_id}", response_model=Donor)
async def update_donor_info(donor_id: str, donor: DonorUpdate, current_user: User = Depends(get_current_user)):
    """
    updates a donor's information
    Args:
        donor_id: ID of the donor to be updated
        donor: donor data to be updated
        current_user: logged-in user, obtained through dependency injection
    Returns:
        dict: a dictionary containing the updated donor's details
    """
    existing_donor = await get_donor_by_id(donor_id)
    if not existing_donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    if existing_donor["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this donor")
    updated_donor = await update_donor(donor_id, donor)
    if not updated_donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return updated_donor

@router.delete("/donors/{donor_id}", response_model=dict)
async def delete_donor_info(donor_id: str, current_user: User = Depends(get_current_user)):
    """
    deletes a donor by ID
    Args:
        donor_id: ID of the donor to be deleted
        current_user: logged-in user, obtained through dependency injection
    Returns:
        dict: a dictionary containing a success message
    """
    donor = await get_donor_by_id(donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    if donor["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this donor")
    deleted = await delete_donor(donor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Donor not found")
    return {"message": "Donor deleted successfully"}
