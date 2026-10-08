import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "markaz-super-secret-key-2026-pakistan")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///markaz.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
