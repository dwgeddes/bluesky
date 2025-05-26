"""
Authentication utilities for BlueSky.

This module provides functions to manage user authentication with the BlueSky service,
including secure credential storage and retrieval.
"""

import logging
from getpass import getpass
from typing import Any, Optional

import keyring
from atproto.exceptions import AtProtocolError

from .config import CREDENTIALS_STORED_MESSAGE, SERVICE_NAME, STORE_CREDENTIALS_PROMPT


def get_credentials(service_name: str, username: str) -> str:
    """
    Get stored credentials or prompt the user for new ones.

    Args:
        service_name: The service name to use in the keyring
        username: The username to authenticate

    Returns:
        The password for the specified username
    """
    try:
        # Check for stored username and password
        stored_username: Optional[str] = keyring.get_password(service_name, "username")
        if stored_username:
            password: Optional[str] = keyring.get_password(
                service_name, stored_username
            )
            if password:
                return password

        # Prompt for new password
        password = getpass(f"Enter your {service_name} password: ")

        # Offer to store credentials
        if input(STORE_CREDENTIALS_PROMPT).strip().lower() == "y":
            set_credentials(service_name, username, password)

        return password
    except Exception as e:
        logging.error(f"Keyring access error: {e}", exc_info=True)
        print(f"Warning: Could not access secure keyring: {e}")
        # Fall back to password prompt if keyring fails
        return getpass(f"Enter your {SERVICE_NAME} password: ")


def clear_credentials() -> None:
    """
    Clear stored credentials from the keyring.
    """
    try:
        stored = keyring.get_password(SERVICE_NAME, "username")
        if stored:
            # Delete the stored username
            keyring.delete_password(SERVICE_NAME, "username")
            # Delete the stored password
            keyring.delete_password(SERVICE_NAME, stored)
            print("Credentials removed from keychain.")
        else:
            print("No stored credentials found.")
    except Exception as e:
        logging.error(f"Error clearing credentials: {e}", exc_info=True)
        print(f"Error clearing credentials: {e}")


def authenticate_bluesky(client: Any, username: str, password: str) -> None:
    """
    Authenticate with BlueSky using the provided credentials.

    Args:
        client: The BlueSky client to authenticate
        username: The username to authenticate with
        password: The password for authentication

    Raises:
        AtProtocolError: If authentication fails due to an AT Protocol error
        Exception: If authentication fails for any other reason
    """
    try:
        client.login(username, password)
        logging.info(f"Successfully authenticated as {username}")
    except AtProtocolError as e:
        logging.error(f"Authentication failed (AtProtocolError): {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Authentication failed: {e}", exc_info=True)
        raise


def set_credentials(service_name: str, username: str, password: str) -> None:
    """
    Store credentials in the keyring.
    """
    keyring.set_password(service_name, "username", username)
    keyring.set_password(service_name, username, password)
    print(CREDENTIALS_STORED_MESSAGE.format(username=username))
