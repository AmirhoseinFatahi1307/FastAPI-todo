from fastapi import APIRouter, Path, Depends, HTTPException, Body, Query, status
from fastapi.responses import JSONResponse
from users.schema import *
from users.models import User_Model
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db: Session = Depends(get_db),
):
    user_obj = db.query(User_Model).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user doesn't exist"
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid"
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
