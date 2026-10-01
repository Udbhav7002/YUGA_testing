from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from middleware import install_crash_interceptor
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Auth Service API", version="1.0.0")

# CodeGhost crash interceptor (HMAC-signed reports + Presidio scrubbing)
install_crash_interceptor(app)

# Mock Database
USERS_DB = {
    1: {"id": 1, "username": "admin", "role": "superuser"},
    2: {"id": 2, "username": "john", "role": "user"}
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(req: LoginRequest):
    if req.username == "admin" and req.password == "secret":
        return {"token": "fake-jwt-token-1"}
    elif req.username == "john" and req.password == "password":
        return {"token": "fake-jwt-token-2"}
    raise HTTPException(status_code=401, detail="Unauthorized")

def fetch_user_from_db(user_id: int):
    user_record = USERS_DB.get(user_id)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_record

@app.get("/profile/{user_id}")
async def get_profile(user_id: int):
    """
    Fetches a user profile. Crashes if user doesn't exist.
    """
    user = fetch_user_from_db(user_id)
    return {"status": "success", "user": user}