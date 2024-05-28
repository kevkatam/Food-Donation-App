from fastapi import APIRouter, Depends, HTTPException
from app.models.recipient import Recipient, RecipientCreate, create_recipient
from app.routes.auth import get_current_user
from app.models.user import User


router = APIRouter()


@router.post("/recipients/", response_model=Recipient)
async def create_recipient_endpoint(recipient: RecipientCreate, current_user: User = Depends(get_current_user)):
    """creates a new recipient, allows a recipient user to create a new
    by probiding necessary recipient data
    Args:
        recipient: recipient data to be created
        current_user: current logged_in user, obtained through dependency
        injection
    Returns:
        dict: a dictionary containing the created recipients's details.
    Raises:
        HTTPException: if there is an error in recipient creation
    """
    recipient_id = await create_recipient(recipient, user_id=current_user["id"])
    return {"id": recipient_id, "name": recipient.name, "user_id": current_user["id"]}
