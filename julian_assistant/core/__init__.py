"""Core module for Julian Assistant"""

from .config import config, Config
from .database import db, Database

__all__ = ["config", "Config", "db", "Database"]
