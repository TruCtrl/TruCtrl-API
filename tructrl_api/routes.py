"""
File:         routes.py
Module:       tructrl_api
Project:      TruCtrl-API
Copyrigh:     © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:      MIT
Description:  API routes for the TruCtrl-API application.
"""
from fastapi import APIRouter
from .auth import auth_router
from .users import users_router


# --- Routers ---
api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
