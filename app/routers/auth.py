from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.OAuth import create_access_token
from app.passwordUtils import validate
from app.schemas import Token

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Authenticates a user and returns an access token.

    - **email**: The email of the user.
    - **password**: The password of the user.
    - **db**: The database session.

    Returns:
    - An access token if the authentication is successful.

    Raises:
    - HTTP 403: If the credentials are invalid.
    """
    # Check if the user exists in the database
    user = db.query(User).filter(User.email == email).first()
    
    # If user doesn't exist, raise HTTP 403 error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Validate the provided password
    if not validate(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create an access token if credentials are valid
    access_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
