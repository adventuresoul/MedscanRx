from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter, Form, File
from app import database, passowrdUtils, schemas, models
from app.database import get_db
from sqlalchemy.orm import Session
from app.OAuth import get_current_user
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

### Users route
@router.get("/", response_model = List[schemas.UserBase])
async def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

# create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def create_user(username: str = Form(...),
                email: str = Form(...),
                contact: str = Form(...),
                password: str = Form(...), 
                db: Session = Depends(get_db)):
    # Hash the password
    hashed_pass = passowrdUtils.password_hash(password)
    # Create a new user with profile picture
    new_user = models.User(username = username, email = email, phone = contact, password = hashed_pass)
    # Add user to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        return {"message": "New user created succesfully"}

# query a user
@router.get("/{id}", response_model = schemas.User)
async def get_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # if user doesn't exist, raise Http error
    if not user:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    # else return the user
    return user

# Forgot passsword
@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Message)
async def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    pass

# delete a user
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user():
    pass