"""
Creator HQ Configuration
"""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "creatorhq-dev")

    APP_NAME = "Creator HQ"
    VERSION = "2.0.0 Foundation"
