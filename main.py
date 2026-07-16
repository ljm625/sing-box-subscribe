"""Vercel WSGI entrypoint.

The configuration generator lives in generate_config.py. Keeping this module
web-only prevents Vercel from treating the CLI implementation as a Flask app.
"""

from api.app import app


__all__ = ["app"]
