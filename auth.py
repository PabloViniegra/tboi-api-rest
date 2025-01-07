from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_AUTHORIZATION = os.getenv("API_KEY_AUTHORIZATION")

if not API_KEY_AUTHORIZATION:
    raise Exception(
        "No API key found. Add it to a .env file as API_KEY_AUTHORIZATION.")

api_key_header = APIKeyHeader(name="X-API-Key")


def get_user(api_key: str = Security(api_key_header)):
    if api_key != API_KEY_AUTHORIZATION:
        raise HTTPException(
            status_code=401, detail="Missing or invalid API Key.")
    return {"user": "authenticated_user"}
