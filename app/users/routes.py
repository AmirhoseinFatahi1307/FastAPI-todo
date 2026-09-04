from fastapi import APIRouter, Path, Depends, HTTPException, Body, Query, status
from fastapi.responses import JSONResponse
from users.schema import *
from users.models import User_Model, TokenModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

router = APIRouter(tags=["Users"], prefix="/users")


def generate_toke(lenght=32):
    return secrets.token_hex(lenght)


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db: Session = Depends(get_db),
):
    user_obj = db.query(User_Model).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid"
        )

    # Token base authentication
    # token_obj = TokenModel(user_id=user_obj.id, token=generate_toke())
    # db.add(token_obj)
    # db.commit()
    # db.refresh(token_obj)
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
):
    if db.query(User_Model).filter_by(username=request.username.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already exist"
        )
    user_obj = User_Model(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail": "User registered successfully"})


@router.post("/refresh_token")
async def user_refresh_token(
    request: UserRefreshTokenSchema,
    db: Session = Depends(get_db),
):
    user_id = decode_refresh_token(request.token)

    user_obj = db.query(User_Model).filter_by(id=user_id).one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed, user not found",
        )

    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access_token": access_token})
