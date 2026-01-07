"""
Database models and utilities for Julian Assistant
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .config import config

# Create base class for models
Base = declarative_base()


class Schedule(Base):
    """Model for schedule/calendar entries"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    location = Column(String(200))
    priority = Column(String(20), default="medium")  # low, medium, high
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FinanceTransaction(Base):
    """Model for financial transactions"""
    __tablename__ = "finance_transactions"
    
    id = Column(Integer, primary_key=True)
    transaction_type = Column(String(20), nullable=False)  # income, expense
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="IDR")
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    payment_method = Column(String(50))  # cash, credit_card, bank_transfer, etc.
    tags = Column(String(200))  # comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkTask(Base):
    """
    Model for work tasks
    
    Note: This model is defined for future expansion. A WorkManager module
    can be added later to provide task management capabilities.
    """
    __tablename__ = "work_tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")  # low, medium, high
    status = Column(String(20), default="todo")  # todo, in_progress, completed
    due_date = Column(DateTime)
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    tags = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConversationHistory(Base):
    """Model for conversation history"""
    __tablename__ = "conversation_history"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100))
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Database:
    """Database management class"""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection"""
        self.database_url = database_url or config.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create all tables
        Base.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()


# Global database instance
db = Database()
