from ytmusicapi import YTMusic, OAuthCredentials
import json


def load_oauth_credentials(client_secrets_file: str) -> OAuthCredentials:
    """Load OAuth credentials from client secrets file."""
    with open(client_secrets_file, "r") as f:
        client_secrets = json.load(f)

    return OAuthCredentials(
        client_id=client_secrets["installed"]["client_id"],
        client_secret=client_secrets["installed"]["client_secret"],
    )


def authenticate_ytmusic(
    oauth_file: str, oauth_credentials: OAuthCredentials
) -> YTMusic:
    """Authenticate with YouTube Music API."""
    return YTMusic(oauth_file, oauth_credentials=oauth_credentials)
