import os
import logging
import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# --- LOGGING ---
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# --- ENVIRONMENT VARIABLES ---
ENV = os.getenv("APP_ENV", "development")
logger.info(f"App starting in {ENV} mode.")

# --- APP SETUP ---
app = FastAPI(title="User Management API")

# Fake database (dictionary)
users_db = {}

# Data validation model
class User(BaseModel):
    name: str
    email: str

# --- ENDPOINTS ---

# 1. ADD a user (POST)
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def add_user(user_id: int, user: User):
    if user_id in users_db:
        logger.warning(f"Add failed: User {user_id} exists.")
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_db[user_id] = user.model_dump()
    logger.info(f"User {user_id} added.")
    return {"message": "User added", "user": users_db[user_id]}

# 2. FETCH a user (GET)
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def fetch_user(user_id: int):
    if user_id not in users_db:
        logger.error(f"Fetch failed: User {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User {user_id} fetched.")
    return users_db[user_id]

# 3. UPDATE a user (PUT)
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        logger.error(f"Update failed: User {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id] = user.model_dump()
    logger.info(f"User {user_id} updated.")
    return {"message": "User updated", "user": users_db[user_id]}

# 4. DELETE a user (DELETE)
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users_db:
        logger.error(f"Delete failed: User {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    logger.info(f"User {user_id} deleted.")
    return