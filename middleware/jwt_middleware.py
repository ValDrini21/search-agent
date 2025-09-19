import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from typing import Dict, Any

# Load environment variables from .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))

JWT_SECRET = os.getenv("JWT_SECRET")

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    Returns user information from the token
    """
    if not JWT_SECRET:
        raise HTTPException(status_code=500, detail="JWT secret not configured")

    try:
        # Decode the JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        # Extract user information
        user_info = {
            "user_id": payload.get("id"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "tier": payload.get("tier"),
            "next_activity_update": payload.get("next_activity_update")
        }

        return user_info
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def extract_token_from_header(auth_header: str) -> str:
    """
    Extract token from Authorization header
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header must start with 'Bearer '")

    return auth_header.split(" ")[1]
