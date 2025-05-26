"""
Configuration constants for the BlueSky social media client.
"""

# Service configuration
SERVICE_NAME = "Bluesky"
DEFAULT_USERNAME = "jetsetjaxon.bsky.social"

# BlueSky API limits
MAX_POST_LENGTH = 300  # BlueSky post character limit
MAX_IMAGE_SIZE = 1_000_000  # 1MB image size limit

# Image processing
DEFAULT_JPEG_QUALITY = 85

# User interaction messages
STORE_CREDENTIALS_PROMPT = "Store credentials in keychain? (y/n): "
CREDENTIALS_STORED_MESSAGE = "Credentials for {username} stored securely."

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_LOG_LEVEL = "ERROR"
