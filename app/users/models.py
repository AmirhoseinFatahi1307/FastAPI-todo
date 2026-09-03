from sqlalchemy import (
    func,
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
)
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User_Model(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    tasks = relationship("Task_models", back_populates="user")

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    token = Column(String, nullable=False, unique=True)
    create_date = Column(DateTime, server_default=func.now())

    user = relationship("User_Model", uselist=False)
