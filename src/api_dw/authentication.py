import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
API_TOKEN = os.getenv("TOKEN")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        #print("Token loaded from .env:", repr(API_TOKEN))
        #print("Verifying token:", token)  # Log of the received token
        if token.strip() != API_TOKEN.strip():
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": "Valid token"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))