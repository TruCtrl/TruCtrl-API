# SPDX-FileCopyrightText: 2025 McGuire Technology, LLC and TruCtrl Contributors
# SPDX-License-Identifier: MIT
#
# SPDX-FileComment: This file is the main entry point for the TruCtrl-API FastAPI application.
# It sets up the FastAPI app, configures logging, and includes the main API router.
# All global exception handling and application-level configuration is performed here.

import logging
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from config import config
from routes import api_router

# --- Logging ---
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger(config.app_name)

# --- App Factory ---
def create_app() -> FastAPI:
    app = FastAPI(
        title=config.app_name,
        version=config.version,
        debug=config.debug
    )
    app.include_router(api_router)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )

    return app

app = create_app()


# --- Entry Point Check ---
if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, reload=True)
