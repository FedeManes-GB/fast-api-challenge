from fastapi import status
from sqlalchemy import inspect

from crud_challenge.models_db import User


def user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "role": user.role,
        "active": user.active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }


def test_list_users(client, test_user):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [user_to_dict(test_user)]


def test_get_user_success(client, test_user):
    response = client.get("users/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_to_dict(test_user)


def test_get_user_fail(client, test_user):
    response = client.get("users/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_create_user_succesfull(client, test_user, test_db):
    user_request = {
        "active": True,
        "email": "fedePost@gmail.com",
        "first_name": "Federico",
        "last_name": "Test",
        "role": "admin",
        "username": "fedePost",
    }
    response = client.post("/users/create", json=user_request)
    assert response.status_code == 201

    user_created = test_db.query(User).filter(User.id == 2).first()

    assert user_created.email == user_request["email"]


def test_create_user_fail(client, test_user, test_db):
    user_request = {
        "active": True,
        "email": "fede1234@gmail.com",
        "first_name": "Federico",
        "last_name": "Test",
        "role": "admin",
        "username": "fedePost",
    }
    response = client.post("/users/create", json=user_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_update_user_succesfull(client, test_user, test_db):
    user_request = {
        "email": "fedePut@gmail.com",
    }
    response = client.put("/users/update/1", json=user_request)
    assert response.status_code == 204

    user_updated = test_db.query(User).filter(User.id == 1).first()
    assert user_updated.email == user_request["email"]


def test_update_user_fail(client, test_user, test_db):
    user_request = {
        "email": "fedePut@gmail.com",
    }
    response = client.put("/users/update/999", json=user_request)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_succesfull(client, test_user, test_db):
    response = client.delete("/users/delete/1")
    assert response.status_code == 204
    user_deleted = test_db.query(User).filter(User.id == 1).first()
    assert user_deleted is None


def test_delete_user_fail(client, test_user, test_db):
    response = client.delete("/users/delete/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_db_is_clean(test_db):
    inspector = inspect(test_db.bind)
    tables = inspector.get_table_names()
    user_count = test_db.query(User).count()

    assert "users" in tables
    assert user_count == 0
