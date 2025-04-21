from datetime import datetime

from fastapi import FastAPI, HTTPException, Path, status

from .database import db_dependency
from .models_db import User
from .models_pydantic import UserCreate, UserRequest, UserUpdate
from .util_logger import logger

logger.info("Starting FastAPI application...")
app = FastAPI()
logger.info("FastAPI Running")


@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserCreate])
def list_users(db: db_dependency):
    try:
        logger.info("Fetching all users")
        all_users = db.query(User).all()
        logger.info("All users fetched succesfully")
        return all_users
    except Exception as e:
        logger.error(
            f"An error occurred requesting /users endpoint: {e}", exc_info=True
        )
        raise


@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserCreate)
def get_user(db: db_dependency, id: int = Path(gt=0)):
    try:
        logger.info(f"Fetching user with id: {id}")
        find_user = db.query(User).filter(User.id == id).first()
        if find_user is not None:
            logger.info(f"User with id: {id} fetched")
            return find_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(
            f"An error occurred requesting /users/:id endpoint: {e}", exc_info=True
        )
        raise


@app.post(
    "/users/create", status_code=status.HTTP_201_CREATED, response_model=UserCreate
)
def create_user(db: db_dependency, input_user: UserRequest):
    try:
        logger.info(f"Creating user with body: {input_user.model_dump_json()}")
        existing_user = db.query(User).filter(User.email == input_user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(**input_user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        created_user = db.query(User).filter(User.email == input_user.email).first()
        logger.info("User created succesfully")
        return created_user
    except Exception as e:
        logger.error(
            f"An error occurred requesting /users/create endpoint: {e}", exc_info=True
        )
        raise


@app.put(
    "/users/update/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_users(db: db_dependency, update_user: UserUpdate, id: int = Path(gt=0)):
    try:
        logger.info(f"Updating user with id: {id}")
        user_to_update = db.query(User).filter(User.id == id).first()
        if user_to_update is not None:
            user_to_update.updated_at = datetime.now()
            for key, value in update_user.model_dump(exclude_unset=True).items():
                if hasattr(user_to_update, key):
                    setattr(user_to_update, key, value)
            db.add(user_to_update)
            db.commit()
            db.refresh(user_to_update)
            updated_user = db.query(User).filter(User.id == id).first()
            logger.info(f"User with id: {id} updated succesfully")
            return updated_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(
            f"An error occurred requesting /users/update/:id endpoint: {e}",
            exc_info=True,
        )
        raise


@app.delete("/users/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: db_dependency, id: int = Path(gt=0)):
    try:
        logger.info(f"Deleting user with id: {id}")
        user_to_deleted = db.query(User).filter(User.id == id).first()
        if user_to_deleted is not None:
            db.query(User).filter(User.id == id).delete()
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User with id: {id} deleted succesfully")
    except Exception as e:
        logger.error(
            f"An error occurred requesting /users/delete/:id endpoint: {e}",
            exc_info=True,
        )
        raise
