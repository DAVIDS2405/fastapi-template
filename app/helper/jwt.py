from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")


def create_token(id: str):
    access_token_expires = timedelta(minutes=30)
    expire = datetime.now() + access_token_expires
    access_token = {"user_id": str(id), "expires": str(expire)}
    JWT = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    return JWT


def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if (payload["expires"] < str(datetime.now())):
            raise HTTPException(
                status_code=401,
                detail="Token caducado.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return payload
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido.", headers={
                            "WWW-Authenticate": "Bearer"})
