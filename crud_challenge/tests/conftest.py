import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine

from crud_challenge.database import Base, SessionLocal, get_db
from crud_challenge.main import app
from crud_challenge.models_db import User


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    SessionLocal.configure(bind=engine)

    test_db_session = SessionLocal()

    yield test_db_session

    test_db_session.close()


@pytest.fixture(scope="module")
def app_with_test_db(test_db):
    def custom_get_db():
        yield test_db

    app.dependency_overrides[get_db] = custom_get_db
    yield app
    app.dependency_overrides.pop(get_db)


@pytest.fixture
def client(app_with_test_db):
    return TestClient(app_with_test_db)


@pytest.fixture
def test_user(test_db):
    user = User(
        active=True,
        email="fede1234@gmail.com",
        first_name="Federico",
        last_name="Test",
        role="admin",
        username="fede1234",
    )

    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    yield user

    test_db.query(User).delete()
    test_db.commit()
