import pytest

from bluesky_social.auth import authenticate_bluesky, clear_credentials, get_credentials


class DummyClient:
    def __init__(self):
        self.logged_in = False

    def login(self, username, password):
        if username == "valid" and password == "secret":
            self.logged_in = True
        else:
            raise Exception("Login failed")


def dummy_input(prompt):
    return "n"


def dummy_getpass(prompt):
    return "secret"


def test_get_credentials(monkeypatch):
    monkeypatch.setattr(
        "bluesky_social.auth.getpass", lambda prompt: dummy_getpass(prompt)
    )
    monkeypatch.setattr("builtins.input", lambda prompt: dummy_input(prompt))
    monkeypatch.setattr("bluesky_social.auth.keyring.get_password", lambda s, u: None)
    creds = get_credentials("Bluesky", "valid")
    assert creds == "secret"


def test_clear_credentials(monkeypatch):
    monkeypatch.setattr(
        "bluesky_social.auth.keyring.get_password", lambda s, u: "stored_user"
    )
    monkeypatch.setattr(
        "bluesky_social.auth.keyring.delete_password", lambda s, u: None
    )
    clear_credentials()


def test_authenticate_bluesky_success():
    client = DummyClient()
    authenticate_bluesky(client, "valid", "secret")
    assert client.logged_in


def test_authenticate_bluesky_failure():
    client = DummyClient()
    with pytest.raises(Exception):
        authenticate_bluesky(client, "wrong", "pw")
