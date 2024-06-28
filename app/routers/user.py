from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter, Form
from app import database, passwordUtils, schemas, models
from app.database import get_db
from sqlalchemy.orm import Session
from app.OAuth import get_current_user
from typing import List
import os

admin = os.getenv("ADMIN")
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

### Users route
@router.get("", response_model=List[schemas.UserBase])
async def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieve all registered users.

    - **db**: The database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - List of all users.

    Raises:
    - HTTP 401: If the current user is not the admin.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't have permission to view")

    users = db.query(models.User).all()
    return users

# Create a user
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """
    Create a new user.

    - **username**: The username of the new user.
    - **email**: The email of the new user.
    - **contact**: The contact number of the new user.
    - **password**: The password of the new user.
    - **db**: The database session.

    Returns:
    - A message confirming user creation.

    Raises:
    - HTTP 409: If the user already exists.
    """
    hashed_pass = passwordUtils.password_hash(password)
    new_user = models.User(username=username, email=email, phone=contact, password=hashed_pass)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    return {"message": "New user created successfully"}

# Query a user
@router.get("/id", response_model=schemas.User)
async def get_user(id: str = Form(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieve a specific user by ID. Only accessible by admin.

    - **id**: The unique identifier of the user.
    - **db**: The database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - The user's details.

    Raises:
    - HTTP 401: If the current user is not the admin.
    - HTTP 404: If the user is not found.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't have permission to view")
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={id} not found")
    
    return user

# Check if a user exists
@router.post("/check-existance", status_code=status.HTTP_200_OK)
async def check_user(email: str = Form(...), db: Session = Depends(get_db)):
    """
    Check if a user with the given email exists.

    - **email**: The email to check.
    - **db**: The database session.

    Returns:
    - A message confirming the user's existence.

    Raises:
    - HTTP 404: If the user is not found.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
    
    return {"message": "User exists"}

# Update user profile
@router.put("/me", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def update_user_profile(
    username: str = Form(None),
    new_email: str = Form(None),
    new_contact: str = Form(None),
    new_password: str = Form(None), 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Update the current user's profile.

    - **username**: The new username.
    - **new_email**: The new email.
    - **new_contact**: The new contact number.
    - **new_password**: The new password.
    - **db**: The database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - A message confirming the profile update.

    Raises:
    - HTTP 404: If the user is not found.
    """
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if username:
        user.username = username
    if new_email:
        user.email = new_email
    if new_contact:
        user.phone = new_contact
    if new_password:
        user.password = passwordUtils.password_hash(new_password)
    
    db.commit()
    
    return {"message": "User's profile updated successfully"}

# Forgot password
@router.post("/reset-password", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def reset_password(email: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    """
    Reset a user's password.

    - **email**: The email of the user.
    - **new_password**: The new password.
    - **db**: The database session.

    Returns:
    - A message confirming the password reset.

    Raises:
    - HTTP 404: If the user is not found.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
    
    hashed_password = passwordUtils.password_hash(new_password)
    user.password = hashed_password
    db.commit()
    
    return {"message": "User's password updated successfully"}

# Delete a user
@router.delete("", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def delete_user(email: str = Form(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Delete a user. Only accessible by admin.

    - **email**: The email of the user to be deleted.
    - **db**: The database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - A message confirming the user's deletion.

    Raises:
    - HTTP 401: If the current user is not the admin.
    - HTTP 404: If the user is not found.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Method forbidden")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}
