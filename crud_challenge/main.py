from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models_db import Base, User
from .models_pydantic import UserRequest, UserUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
def list_users(db: db_dependency):
    return db.query(User).all()


@app.get("/users/{id}", status_code=status.HTTP_200_OK)
def get_user(db: db_dependency, id: int = Path(gt=0)):
    find_user = db.query(User).filter(User.id == id).first()
    if find_user is not None:
        return find_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, input_user: UserRequest):
    existing_user = db.query(User).filter(User.email == input_user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    all_users = db.query(User).all()
    new_id = 1 if len(all_users) == 0 else all_users[-1].id + 1
    new_user = User(id=new_id, **input_user.model_dump())
    db.add(new_user)
    db.commit()


@app.put("/users/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_users(db: db_dependency, update_user: UserUpdate, id: int = Path(gt=0)):
    user_to_update = db.query(User).filter(User.id == id).first()
    if user_to_update is not None:
        user_to_update.updated_at = datetime.now()
        for key, value in update_user.model_dump(exclude_unset=True).items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)
        db.add(user_to_update)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: db_dependency, id: int = Path(gt=0)):
    user_to_deleted = db.query(User).filter(User.id == id).first()
    if user_to_deleted is not None:
        db.query(User).filter(User.id == id).delete()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")
