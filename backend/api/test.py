from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid

app = FastAPI(title="User Management API")

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    age: Optional[int] = None
    is_active: bool = True

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    age: Optional[int] = None

users_db = {}

@app.get("/")
def read_root():
    return {"message": "User Management API"}

@app.post("/users", response_model=User)
def create_user(user_data: CreateUserRequest):
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        age=user_data.age
    )
    users_db[user_id] = user
    return user

@app.get("/users", response_model=List[User])
def get_users(active_only: bool = False):
    if active_only:
        return [user for user in users_db.values() if user.is_active]
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: CreateUserRequest):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    user.username = user_update.username
    user.email = user_update.email
    user.age = user_update.age
    return user