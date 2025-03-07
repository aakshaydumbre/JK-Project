from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from intelligent_book_manager.app.services.auth import authenticate_user, create_access_token

router = APIRouter()

@router.post("/get_token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate an access token for a valid user.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
