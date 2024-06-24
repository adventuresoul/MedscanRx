from pydantic import BaseModel, EmailStr

# file_path
class FilePath(BaseModel):
    path: str


## Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str
    class Config:
        orm_mode = True

# request model
class UserCreate(UserBase):
    password: str

# request model
class UpdateUser(UserBase):
    password: str

# response model
class User(UserBase):
    class Config:
        orm_mode = True

# Login model
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

# Messages
class Message(BaseModel):
    message: str
