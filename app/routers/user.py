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
@router.get("/", response_model=List[schemas.UserBase])
async def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Returns the list of all registered users of the application.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't have permission to view")

    users = db.query(models.User).all()
    return users

# Create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """
    Creates a new user.
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
@router.get("/user", response_model=schemas.User)
async def get_user(id: str = Form(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieves a specific user by ID. Only admin can access this.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't have permission to view")
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={id} not found")
    
    return user

# Check if a user exists
@router.post("/check", status_code=status.HTTP_200_OK)
async def check_user(email: str = Form(...), db: Session = Depends(get_db)):
    """
    Checks if a user with the given email exists.
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
    Updates the current user's profile.
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
@router.post("/reset_password", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def reset_password(email: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    """
    Resets the user's password.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
    
    hashed_password = passwordUtils.password_hash(new_password)
    user.password = hashed_password
    db.commit()
    
    return {"message": "User's password updated successfully"}

# Delete a user
@router.delete("/", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def delete_user(email: str = Form(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Deletes a user. Only admin can perform this action.
    """
    if current_user.email != admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Method forbidden")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}
