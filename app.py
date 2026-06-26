"""
Creator HQ
Application Entry Point

Copyright (c) 2026 Mike Cocita
MIT License
"""

from creatorhq import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
