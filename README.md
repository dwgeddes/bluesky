# Bluesky Social

A Python client for interacting with the BlueSky social network through both a command-line interface and a programmatic API.

## Features

- Post text and images to BlueSky
- Support for hashtags in posts
- View and manage notifications
- List and respond to replies
- Secure credential storage using system keychain
- Image format conversion and optimization

## Installation

### Standard installation

```bash
pip install bluesky-social
```

### Development installation

```bash
# Clone the repository
git clone https://github.com/dwgeddes/bluesky-social.git
cd bluesky-social

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the package in development mode
pip install -e '.[dev]'
```

## Command-Line Usage

The package provides a command-line interface for common BlueSky operations:

```bash
# Post a text message
bluesky --text "Hello BlueSky! #FirstPost"

# Post with an image
bluesky --text "Check out this photo" --image path/to/image.jpg --alt "Description of image"

# Get notifications
bluesky --get-notifications

# List unanswered responses to your posts
bluesky --get-responses

# List your posts and their responses
bluesky --list-posts

# Clear stored credentials
bluesky --clear-credentials

# Use a different BlueSky account
bluesky --username "your-username.bsky.social" --text "Posting from another account"
```

## Programmatic Usage

You can also use the library programmatically in your Python code:

```python
from atproto import Client
from bluesky_social.auth import authenticate_bluesky
from bluesky_social.bluesky_core import post

# Authenticate
client = Client()
authenticate_bluesky(client, "your-username.bsky.social", "your-password")

# Post text with hashtags
post(client, "Hello world! #Python #BlueSky")

# Post with an image
post(client, "Check out this photo", image_path="path/to/image.jpg", alt_text="Description of image")
```

## Package Structure

The package is organized into the following modules:

- `bluesky_social.auth`: Authentication utilities with secure credential storage
- `bluesky_social.bluesky_core`: Core posting functionality and hashtag processing
- `bluesky_social.notifications`: Functions to retrieve and manage notifications and responses
- `bluesky_social.image_utils`: Image processing and format conversion
- `bluesky_social.cli`: Command-line interface implementation

## Error Handling

The library provides robust error handling with:

- Specific exception types for different error scenarios
- Detailed error messages for troubleshooting
- Logging of errors to help with debugging

## Development

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bluesky_social
```

### Code formatting and linting

```bash
# Format code with black
black bluesky_social tests

# Lint code with ruff
ruff check bluesky_social tests

# Type checking with mypy
mypy bluesky_social
```

## Dependencies

- `atproto`: Client library for the AT Protocol (BlueSky)
- `Pillow`: For image processing and format conversion
- `keyring`: For secure credential storage

## License

MIT License
