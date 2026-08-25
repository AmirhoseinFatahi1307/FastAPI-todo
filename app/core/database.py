from sqlalchemy import create_engine

from config import settings


from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
