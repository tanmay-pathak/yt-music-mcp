from ytmusicapi import YTMusic
import json
from typing import List, Dict
from fastmcp import FastMCP
from auth import load_oauth_credentials, authenticate_ytmusic
from playlist import get_or_create_playlist, search_songs, add_songs_to_playlist

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
