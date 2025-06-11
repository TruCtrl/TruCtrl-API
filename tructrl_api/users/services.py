"""
File:           servcies.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Services Layer for User Management.
                Contains business logic and operations that act on your models.
                Implements higher-level operations, such as bulk create, update, delete, or more complex workflows.
                Sits between the API routes and the database/ORM layer, making your code more modular and testable.
"""

from sqlmodel import Session
from .models import User

def create_users(session: Session, users_data: list[dict]) -> list[User]:
    users = [User(**data) for data in users_data]
    session.add_all(users)
    session.commit()
    for user in users:
        session.refresh(user)
    return users

def get_users(session: Session, user_ids: list[str]) -> list[User]:
    statement = session.query(User).filter(User.id.in_(user_ids))
    return statement.all()

def update_users(session: Session, users_data: list[dict]) -> list[User]:
    updated_users = []
    for data in users_data:
        user = session.get(User, data['id'])
        if user:
            for key, value in data.items():
                if key != 'id' and hasattr(user, key):
                    setattr(user, key, value)
            session.add(user)
            updated_users.append(user)
    session.commit()
    for user in updated_users:
        session.refresh(user)
    return updated_users

def delete_users(session: Session, user_ids: list[str]) -> int:
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    for user in users:
        session.delete(user)
    session.commit()
    return len(users)

def get_user_by_email(session: Session, email: str) -> User:
    return session.query(User).filter(User.email == email).first()


