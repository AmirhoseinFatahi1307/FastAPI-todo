from sqlalchemy import func, Column, String, Integer, Boolean, Text, DATETIME
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User_Model(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    create_date = Column(DATETIME, server_default=func.now())
    update_date = Column(
        DATETIME, server_default=func.now(), server_onupdate=func.now()
    )

    tasks = relationship("Task_models", back_populates="user")

    def set_password(self, plain_password: str) -> None:
        """Hash the given plain-text password and store it."""
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Check whether a plain-text password matches the stored hash."""
        return pwd_context.verify(plain_password, self.password)
