from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from core.database import Base, create_engine, sessionmaker, get_db
from main import app
import pytest
from faker import Faker
from users.models import User_Model
from tasks.models import Task_models
from auth.jwt_auth import generate_access_token

fake = Faker()


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)


# module
@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# module
@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)


# session
@pytest.fixture(scope="session", autouse=True)
def tearup_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# function
@pytest.fixture(scope="package")
def anonymous_client():
    # anonymous user client
    client = TestClient(app)
    yield client


@pytest.fixture(scope="package")
def authorized_client(db_session):
    # authorized user client
    client = TestClient(app)
    user = db_session.query(User_Model).filter_by(username="user_test").one()
    access_token = generate_access_token(user.id)
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):
    user = User_Model(username="user_test")
    user.set_password("1234")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"user created with username {user.username} and id ={user.id}")

    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            Task_models(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )
    db_session.add_all(tasks_list)
    db_session.commit()
    print(f"added 10 tasks for user id {user.id}")
