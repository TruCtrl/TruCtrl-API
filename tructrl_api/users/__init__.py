"""
File:           __init__.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    User Management Module.
                Exports members for easy importing in other parts of the application.
"""

from .models import User
from .schemas import UserCreate, UserRead, UserUpdate
from .services import create_users, get_users, update_users, delete_users, get_user_by_email
from .routes import users_router
from .dependencies import get_user_by_id