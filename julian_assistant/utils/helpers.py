"""
Utility functions for Julian Assistant
"""
from datetime import datetime
from typing import Any, Dict
import json


def format_currency(amount: float, currency: str = "IDR") -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        currency: Currency code
    
    Returns:
        Formatted currency string
    """
    return f"{currency} {amount:,.2f}"


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M") -> str:
    """
    Format datetime object
    
    Args:
        dt: Datetime object
        format_str: Format string
    
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_tags(tags_str: str) -> list:
    """
    Parse comma-separated tags string
    
    Args:
        tags_str: Comma-separated tags
    
    Returns:
        List of tags
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(",")]


def dict_to_json(data: Dict[str, Any], indent: int = 2) -> str:
    """
    Convert dictionary to JSON string
    
    Args:
        data: Dictionary to convert
        indent: JSON indentation
    
    Returns:
        JSON string
    """
    return json.dumps(data, indent=indent, default=str)


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage
    
    Args:
        part: Part value
        total: Total value
    
    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0
    return (part / total) * 100
