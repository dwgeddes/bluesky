import keyring, logging
from getpass import getpass
from atproto.exceptions import AtProtocolError
# ...existing imports if needed...

service_name = "Bluesky"

def get_credentials(service_name: str, username: str) -> str:
    try:
        stored_username = keyring.get_password(service_name, "username")
        if stored_username:
            password = keyring.get_password(service_name, stored_username)
            if password:
                return password
        password = getpass("Enter your BlueSky password: ")
        if input("Store credentials in keychain? (y/n): ").strip().lower() == 'y':
            keyring.set_password(service_name, "username", username)
            keyring.set_password(service_name, username, password)
        return password
    except Exception as e:
        logging.error(f"Keyring access error: {e}", exc_info=True)
        return getpass("Enter your BlueSky password: ")

def clear_credentials() -> None:
    stored = keyring.get_password(service_name, "username")
    if stored:
        keyring.delete_password(service_name, stored)
        print("Credentials removed from keychain.")
    else:
        print("No stored credentials found.")

def authenticate_bluesky(client, username: str, password: str) -> None:
    try:
        client.login(username, password)
    except AtProtocolError as e:
        logging.error(f"Authentication failed (AtProtocolError): {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Authentication failed: {e}", exc_info=True)
        raise
