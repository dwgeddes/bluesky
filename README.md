# Bluesky Social Module

This package provides a Python module for interacting with the BlueSky social networking platform, offering both a command-line interface and core functionality for posting, notifications, and image handling.

## Installation

```bash
pip install .
```

## Usage

### Command-Line Interface

Run the CLI tool:

```bash
bluesky-social --text "Hello BlueSky!"
```

### Programmatic Use

Import and call functions in your Python code:

```python
from bluesky_social.cli import main
```

## Modules

- auth.py: Handles authentication and credential management.
- bluesky_core.py: Core functions for posting and hashtag detection.
- notifications.py: Functions to list notifications and responses.
- image_utils.py: Image conversion utilities.
- cli.py: Entry point for the command-line interface.

## Dependencies

- atproto
- Pillow
- keyring
