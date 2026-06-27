"""
Creator HQ Application Factory
"""

import logging
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("creatorhq.config.Config")

    # Configure logging
    logging.basicConfig(
        filename="logs/creatorhq.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    logging.info("Creator HQ started.")

    # Register Blueprints
    from .blueprints.dashboard import dashboard
    from .blueprints.control import control

    app.register_blueprint(dashboard)
    app.register_blueprint(control)

    return app
