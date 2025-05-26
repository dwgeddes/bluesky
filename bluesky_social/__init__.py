"""
BlueSky Social Media Client

A Python library and CLI for interacting with the BlueSky social network.
"""

from .auth import authenticate_bluesky, clear_credentials, get_credentials
from .bluesky_core import detect_hashtags, post
from .cli import main
from .image_utils import convert_to_jpeg
from .notifications import (
    get_notifications,
    get_responses,
    list_posts_and_responses,
    list_unanswered_responses,
)

__version__ = "0.1.0"
__author__ = "David Geddes"
__email__ = "dwgeddes@gmail.com"

__all__ = [
    # Core functionality
    "post",
    "detect_hashtags",
    # Authentication
    "authenticate_bluesky",
    "get_credentials",
    "clear_credentials",
    # Notifications and responses
    "get_notifications",
    "get_responses",
    "list_posts_and_responses",
    "list_unanswered_responses",
    # Image utilities
    "convert_to_jpeg",
    # CLI
    "main",
]
