import time
import jwt
from decouple import config

JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")


# Function return generated tokens (jwts)
def token_response(token: str):
    return {
        "access_token": token
    }


# Function used for signing the JWT string
def sign_token(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600,
    }
    token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}
