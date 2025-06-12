"""
File:         __init__.py
Module:       users
Description:  API authentication module for the TruCtrl-API application.
Project:      TruCtrl-API
Copyrigh:     © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:      MIT
"""

from .routes import router
from .models import (
    Token, 
    TokenData
)