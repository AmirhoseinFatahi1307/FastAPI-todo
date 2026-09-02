from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from users.models import User_Model
from core.database import get_db
from sqlalchemy.orm import Session

security = HTTPBasic()


def get_authenticated_user(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user_obj = (
        db.query(User_Model).filter_by(username=credentials.username).one_or_none()
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not user_obj.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_obj
