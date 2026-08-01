import os
import ssl

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "pakexplorer-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    _ssl_context = ssl.create_default_context()
    _ssl_context.check_hostname = False
    _ssl_context.verify_mode = ssl.CERT_NONE

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"ssl": _ssl_context}
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False