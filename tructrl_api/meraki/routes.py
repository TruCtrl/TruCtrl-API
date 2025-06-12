"""
File:           routes.py
Module:         meraki
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    API routes for Meraki integration.
"""
from fastapi import APIRouter
from .organizations.routes import router as organizations_router
#from .networks.routes import networks_router
#from .devices.routes import devices_router

router = APIRouter(prefix="/meraki")

router.include_router(organizations_router, prefix="/organizations", tags=["Meraki Organizations"])
