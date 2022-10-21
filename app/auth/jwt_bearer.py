from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_jwt


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme:
                raise HTTPException(status_code=403, detail="Invalid Or Expired Token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid Or Expired Token!")

    def verify_token(self, jwt: str):
        is_token_valid: bool = False
        payload = decode_jwt(jwt)

        if payload:
            is_token_valid = True
        return is_token_valid
