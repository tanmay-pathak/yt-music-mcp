from ytmusicapi import YTMusic, OAuthCredentials
import json
from typing import List, Tuple, Dict
from fastmcp import FastMCP

mcp = FastMCP("YouTube Music Playlist Creator 🎵")


@mcp.tool()
def add_songs_to_yt_playlist(
    songs: List[Dict[str, str]],
    playlist_title: str = "AI Playlist",
    playlist_description: str = "Songs added via yt-music-mcp.",
) -> Dict[str, any]:
    """
    Add a list of songs to a YouTube Music playlist.

    Args:
        songs: A list of dictionaries, each with 'title' and 'artist' keys
        playlist_title: The title of the playlist to add songs to (creates if not exists)
        playlist_description: The description for the playlist if it needs to be created

    Returns:
        A dictionary containing the playlist ID, added video IDs, and status
    """
    # Configuration
    CLIENT_SECRETS_FILE = "yt_client_secrets.json"
    OAUTH_FILE = "oauth.json"

    # Authentication
    oauth_credentials = load_oauth_credentials(CLIENT_SECRETS_FILE)
    ytmusic = authenticate_ytmusic(OAUTH_FILE, oauth_credentials)

    # Get or create playlist
    playlist_id = get_or_create_playlist(ytmusic, playlist_title, playlist_description)

    # Convert the list of song dictionaries to (title, artist) tuples
    song_tuples = [(song["title"], song["artist"]) for song in songs]

    # Search for songs
    video_ids = search_songs(ytmusic, song_tuples)

    # Add songs to playlist
    status = add_songs_to_playlist(ytmusic, playlist_id, video_ids, playlist_title)

    return {
        "playlist_id": playlist_id,
        "video_ids": video_ids,
        "status": status,
        "song_count": len(video_ids),
    }


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
    not_found = []

    for title, artist in songs:
        result = ytmusic.search(f"{title} {artist}", filter="songs", limit=1)
        if result:
            video_ids.append(result[0]["videoId"])
        else:
            not_found.append(f"{title} by {artist}")

    if not_found:
        print(f"Info: Could not find these songs: {', '.join(not_found)}")

    return video_ids


def add_songs_to_playlist(
    ytmusic: YTMusic, playlist_id: str, video_ids: List[str], playlist_title: str
) -> str:
    """Add songs to the specified playlist and return status message."""
    if not video_ids:
        return "No matches found, no songs were added to the playlist."

    ytmusic.add_playlist_items(playlist_id, video_ids)
    return f"Added {len(video_ids)} tracks to '{playlist_title}'."
