# File:         routes.py
# Package:      tructrl_api
# Project:      TruCtrl
# Copyright:    © 2025 McGuire Technology, LLC and TruCtrl Contributors
# License:      MIT
# Description:  API routes for the TruCtrl-API application.

# --- Imports ---

# Standard Imports

# Third-Party Imports
from fastapi import APIRouter

# Project Imports

# Module Imports
from .auth import router as auth_router
from .entity import router as entity_router
from .meraki import router as meraki_router
from .users import router as users_router



# --- Routers ---

api_router = APIRouter()

package_routers = [
    auth_router, 
    entity_router,
    meraki_router, 
    users_router, 
]

for package_router in package_routers:
    api_router.include_router(package_router)