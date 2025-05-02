from ytmusicapi import YTMusic, OAuthCredentials
import json
from typing import List, Tuple


def load_oauth_credentials(client_secrets_file: str) -> OAuthCredentials:
    """Load OAuth credentials from client secrets file."""
    with open(client_secrets_file, "r") as f:
        client_secrets = json.load(f)
    
    return OAuthCredentials(
        client_id=client_secrets["installed"]["client_id"],
        client_secret=client_secrets["installed"]["client_secret"]
    )


def authenticate_ytmusic(oauth_file: str, oauth_credentials: OAuthCredentials) -> YTMusic:
    """Authenticate with YouTube Music API."""
    return YTMusic(oauth_file, oauth_credentials=oauth_credentials)


def get_or_create_playlist(ytmusic: YTMusic, title: str, description: str) -> str:
    """Get existing playlist ID or create a new one if it doesn't exist."""
    playlist_id = next(
        (
            pl["playlistId"]
            for pl in ytmusic.get_library_playlists()
            if pl["title"] == title
        ),
        None,
    )
    
    if playlist_id is None:
        playlist_id = ytmusic.create_playlist(title, description)
    
    return playlist_id


def search_songs(ytmusic: YTMusic, songs: List[Tuple[str, str]]) -> List[str]:
    """Search for songs and return their video IDs."""
    video_ids = []
    for title, artist in songs:
        result = ytmusic.search(f"{title} {artist}", filter="songs", limit=1)
        if result:
            video_ids.append(result[0]["videoId"])
    
    return video_ids


def add_songs_to_playlist(ytmusic: YTMusic, playlist_id: str, video_ids: List[str], playlist_title: str) -> None:
    """Add songs to the specified playlist."""
    if video_ids:
        ytmusic.add_playlist_items(playlist_id, video_ids)
        print(f"Added {len(video_ids)} tracks to '{playlist_title}'.")
    else:
        print("No matches found.")


def main():
    # Configuration
    SONGS = [
        ("Rolling in the Deep", "Adele"),
        ("Bohemian Rhapsody", "Queen"),
    ]
    PLAYLIST_TITLE = "AI Playlist"
    PLAYLIST_DESCRIPTION = "Songs added via yt-music-mcp."
    CLIENT_SECRETS_FILE = "yt_client_secrets.json"
    OAUTH_FILE = "oauth.json"
    
    # Authentication
    oauth_credentials = load_oauth_credentials(CLIENT_SECRETS_FILE)
    ytmusic = authenticate_ytmusic(OAUTH_FILE, oauth_credentials)
    
    # Get or create playlist
    playlist_id = get_or_create_playlist(ytmusic, PLAYLIST_TITLE, PLAYLIST_DESCRIPTION)
    
    # Search for songs
    video_ids = search_songs(ytmusic, SONGS)
    
    # Add songs to playlist
    add_songs_to_playlist(ytmusic, playlist_id, video_ids, PLAYLIST_TITLE)


if __name__ == "__main__":
    main()
