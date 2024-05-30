from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User, UserCreate, create_user, get_user_by_username
from app.routes.auth import authenticate_user, create_access_token


router = APIRouter()


@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ this endpoint allows users to login and receive an access token
    Request Body:
        form_data: an instance of OAuth2PasswordRequestForm which contains:
            username: the username of the user
            password: tha password of the user
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or passowrd",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=User)
async def register_user(user: UserCreate):
    """ this endpoint allows new users to register
    Requets Body:
        username: name of the user.
        password: password of the user
    """
    db_user = await get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registeared")
    user_dict = await create_user(user)
    user_id = user_dict.get("id")
    return {"id": user_id, "username": user.username}
