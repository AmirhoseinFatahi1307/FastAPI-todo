from sqlalchemy import func, Column, String, Integer, Boolean, Text, DATETIME
from core.database import Base


class Task_models(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)

    create_date = Column(DATETIME, server_default=func.now())
    update_date = Column(
        DATETIME, server_default=func.now(), server_onupdate=func.now()
    )
