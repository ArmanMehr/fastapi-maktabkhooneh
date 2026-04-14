import random

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from auth import generate_jwt_token
from database import Base, get_db
from main import app
from models import Expense, User

engine = create_engine(
    "sqlite:///:memory",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="package", autouse=True)
def db_test_session():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="package", autouse=True)
def override_dependencies(db_test_session):
    app.dependency_overrides[get_db] = lambda: db_test_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="package", autouse=True)
def create_all_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="package", autouse=True)
def sample_data(db_test_session: Session):
    sample_user = User(username="testuser", password="samplepass123")
    db_test_session.add(sample_user)
    db_test_session.commit()
    db_test_session.refresh(sample_user)

    expense_list = []
    for _ in range(10):
        sample_expense = Expense(
            amount=random.randint(1, 1000),
            description="",
            user_id=sample_user.id,
        )
        expense_list.append(sample_expense)

    db_test_session.add_all(expense_list)
    db_test_session.commit()


@pytest.fixture(scope="function", autouse=True)
def annonymus_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def auth_client(db_test_session: Session):
    client = TestClient(app)
    user: User = (
        db_test_session.query(User).filter_by(username="testuser").one()
    )
    access_token = generate_jwt_token("access", user.id)
    client.cookies.set("access_token", access_token)
    return client
