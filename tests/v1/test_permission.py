import sys
from os.path import abspath, dirname, join

# import uuid

sys.path.insert(0, abspath(join(dirname(__file__), "../..")))

import jwt
from decouple import config
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.database import get_db, Base
from main import app

SQLALCHEMY_DATABASE_URL = config("DB_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def admin_token():
    token = jwt.encode({"username": "admin"}, SECRET_KEY, algorithm=ALGORITHM)
    return token


@pytest.fixture(scope="module")
def invalid_token():
    token = jwt.encode({"username": "invalid"}, "invalid_key", algorithm=ALGORITHM)
    return token


def test_create_permission(client, admin_token):
    # Ensure no duplicate permission exists before creation
    response = client.get(
        "/api/v1/permissions", headers={"Authorization": f"Bearer {admin_token}"}
    )
    if response.status_code == 200:
        permissions = response.json()["data"]
        for permission in permissions:
            if permission["name"] == "test_permission":
                client.delete(
                    f"/api/v1/permissions/{permission['id']}",
                    headers={"Authorization": f"Bearer {admin_token}"},
                )

    # Create a new permission
    response = client.post(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "test_permission", "description": "Test permission"},
    )
    if response.status_code != 201:
        print(response.json())  # Print the response content for debugging
    assert response.status_code == 201


def test_create_permission_unauthorized(client, invalid_token):
    response = client.post(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {invalid_token}"},
        json={
            "name": "unauthorized_permission",
            "description": "This should not be created",
        },
    )
    assert (
        response.status_code == 401
    ), f"Expected status code 401, but got {response.status_code}"


def test_get_permissions(client, admin_token):
    response = client.get(
        "/api/v1/permissions", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200


def test_get_permission(client, admin_token):
    response = client.get(
        "/api/v1/permissions", headers={"Authorization": f"Bearer {admin_token}"}
    )
    if response.status_code == 200:
        permissions = response.json()["data"]
        for permission in permissions:
            if permission["name"] == "get_permission":
                client.delete(
                    f"/api/v1/permissions/{permission['id']}",
                    headers={"Authorization": f"Bearer {admin_token}"},
                )

    response = client.post(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "get_permission", "description": "Permission to get"},
    )
    if response.status_code != 201:
        print(response.json())  # Print the response content for debugging
    assert response.status_code == 201

    created_permission = response.json()["data"]
    permission_id = created_permission["id"]

    response = client.get(
        f"/api/v1/permissions/{permission_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_update_permission(client, admin_token):
    response = client.get(
        "/api/v1/permissions", headers={"Authorization": f"Bearer {admin_token}"}
    )
    if response.status_code == 200:
        permissions = response.json()["data"]
        for permission in permissions:
            if permission["name"] == "updated_permission":
                client.delete(
                    f"/api/v1/permissions/{permission['id']}",
                    headers={"Authorization": f"Bearer {admin_token}"},
                )
            if permission["name"] == "update_permission":
                client.delete(
                    f"/api/v1/permissions/{permission['id']}",
                    headers={"Authorization": f"Bearer {admin_token}"},
                )

    response = client.post(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "update_permission", "description": "Permission to update"},
    )
    if response.status_code != 201:
        print(response.json())  # Print the response content for debugging
    assert response.status_code == 201

    created_permission = response.json()["data"]
    permission_id = created_permission["id"]

    response = client.put(
        f"/api/v1/permissions/{permission_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "updated_permission", "description": "Updated permission"},
    )
    if response.status_code != 200:
        print(response.json())  # Print the response content for debugging
    assert response.status_code == 200


def test_delete_permission(client, admin_token):
    response = client.get(
        "/api/v1/permissions", headers={"Authorization": f"Bearer {admin_token}"}
    )
    if response.status_code == 200:
        permissions = response.json()["data"]
        for permission in permissions:
            if permission["name"] == "delete_permission":
                client.delete(
                    f"/api/v1/permissions/{permission['id']}",
                    headers={"Authorization": f"Bearer {admin_token}"},
                )

    response = client.post(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "delete_permission", "description": "Permission to delete"},
    )
    if response.status_code != 201:
        print(response.json())
    assert (
        response.status_code == 201
    ), f"Create permission failed with {response.json()}"

    created_permission = response.json()["data"]
    permission_id = created_permission["id"]

    response = client.delete(
        f"/api/v1/permissions/{permission_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert (
        response.status_code == 200
    ), f"Delete permission failed with {response.json()}"
    print(response.json())
