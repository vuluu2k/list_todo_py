import pprint
from fastapi import Body, Request, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import UserLoginModel, UserModel
from .jwt_handler import sign_token

router = APIRouter()


@router.post("/signup", response_description="register in auth with jwt")
async def signup_user(request: Request, user: UserModel = Body(...)):
    user_db = await request.app.mongodb["users"].find_one({"email": user.email})
    if user_db:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "email is already exist", "success": False})

    new_user = await request.app.mongodb["users"].insert_one(jsonable_encoder(user))
    if (created_user := await request.app.mongodb["users"].find_one({"_id": new_user.inserted_id})) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"access_token": sign_token(user.email), "created_user": created_user,
                                     "success": True})

    raise HTTPException(status_code=404, detail="database had a this user")


@router.post("/signin", response_description="login in auth with jwt")
async def signin_user(request: Request, user: UserLoginModel = Body(...)):
    user_db = await request.app.mongodb["users"].find_one({"email": user.email})

    if user_db and user_db['password'] == user.password:
        return sign_token(user.email)
    else:
        return JSONResponse(content={"error": "Invalid login details!"})
