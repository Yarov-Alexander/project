from http import client

import pytest
from importlib import reload
from app.core.dependcies import get_async_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
import app.main as main

@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread":False}, poolclass="StaticPool")
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False, expire_on_commit=False)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def test_client(test_db):
    def override_get_db():
        yield test_db

    main.app.dependency_overrides[get_async_db] = override_get_db

    try:
        with TestClient(main.app) as test_client:
            yield test_client
    finally:
        main.app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_env(test_client):
    path = tmp_path / "test.env"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{path}")

    reload(main)
    response = client.get("/")
    assert response.status_code == 200

