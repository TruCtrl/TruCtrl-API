from fastapi import Depends
from sqlmodel import Session
from .models import User
from ..database import get_session

def get_user_by_username(username: str, session: Session = Depends(get_session)) -> User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user
