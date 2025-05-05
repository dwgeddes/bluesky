"""
Authentication utilities for BlueSky.

This module provides functions to manage user authentication with the BlueSky service,
including secure credential storage and retrieval.
"""
import logging
from getpass import getpass
from typing import Optional

import keyring
from atproto.exceptions import AtProtocolError

# Constants for service identification
SERVICE_NAME = "Bluesky"

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
        stored_username = keyring.get_password(service_name, "username")
        if stored_username:
            password = keyring.get_password(service_name, stored_username)
            if password:
                return password
        
        # Prompt for new password
        password = getpass("Enter your BlueSky password: ")
        
        # Offer to store credentials
        save_option = input("Store credentials in keychain? (y/n): ").strip().lower()
        if save_option == 'y':
            keyring.set_password(service_name, "username", username)
            keyring.set_password(service_name, username, password)
            print(f"Credentials for {username} stored securely.")
        
        return password
    except Exception as e:
        logging.error(f"Keyring access error: {e}", exc_info=True)
        print(f"Warning: Could not access secure keyring: {e}")
        # Fall back to password prompt if keyring fails
        return getpass("Enter your BlueSky password: ")

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

def authenticate_bluesky(client, username: str, password: str) -> None:
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
