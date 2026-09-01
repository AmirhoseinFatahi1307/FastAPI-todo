from sqlalchemy import (
    func,
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DATETIME,
    ForeignKey,
)
from core.database import Base
from sqlalchemy.orm import relationship


class Task_models(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)

    create_date = Column(DATETIME, server_default=func.now())
    update_date = Column(
        DATETIME, server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("User_Model", back_populates="tasks", uselist=False)
