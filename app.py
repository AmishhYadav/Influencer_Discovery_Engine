"""Root entry point for Vercel deployment.

This file serves as the main entry point for the FastAPI application.
Vercel looks for an 'app' variable in this file to serve the application.
"""

from src.api.main import app

__all__ = ["app"]
