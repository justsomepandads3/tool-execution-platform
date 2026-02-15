"""
FastAPI application factory and setup.

This module creates and configures the FastAPI application instance,
sets up exception handlers, and registers all API routes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.exceptions import ToolExecutionException, ToolNotFoundException
from app.api import routes_system, routes_tools


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Unified execution platform for utility tools",
        version="1.0.0",
    )

    # Configure CORS (allow all origins for development)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Register routes
    app.include_router(routes_system.router)
    app.include_router(routes_tools.router)

    # Root endpoint
    @app.get("/")
    def root():
        """Root endpoint with API information."""
        return {
            "name": settings.APP_NAME,
            "version": "1.0.0",
            "docs": "/docs"
        }

    # Setup logging on startup
    @app.on_event("startup")
    def startup_event():
        """Initialize logging on application startup."""
        logger.info(f"Starting {settings.APP_NAME}")
        logger.info(f"Debug mode: {settings.DEBUG}")

    @app.on_event("shutdown")
    def shutdown_event():
        """Log application shutdown."""
        logger.info(f"Shutting down {settings.APP_NAME}")

    return app


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers for the application.

    Args:
        app: The FastAPI application instance
    """

    @app.exception_handler(ToolNotFoundException)
    async def tool_not_found_handler(request, exc: ToolNotFoundException):
        """Handle tool not found exceptions."""
        logger.warning(f"Tool not found: {exc.message}")
        return {
            "error": exc.message,
            "status_code": 404
        }

    @app.exception_handler(ToolExecutionException)
    async def tool_execution_handler(request, exc: ToolExecutionException):
        """Handle tool execution exceptions."""
        logger.error(f"Tool execution error: {exc.message}")
        return {
            "error": exc.message,
            "status_code": 500
        }

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
        return {
            "error": exc.detail,
            "status_code": exc.status_code
        }

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        """Handle unexpected exceptions (don't expose details)."""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return {
            "error": "An unexpected error occurred",
            "status_code": 500
        }


# Create the application instance
app = create_app()
