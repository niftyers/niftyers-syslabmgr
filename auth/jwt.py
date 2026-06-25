# app/auth/jwt.py

from jose import jwt
from datetime import datetime, timedelta

SECRET = "secret"

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=8)

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET)