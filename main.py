from typing import List, Dict
from fastmcp import FastMCP
from ytmusic_service import YTMusicService

mcp = FastMCP("YouTube Music Playlist Creator 🎵")
ytmusic_service = YTMusicService()


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
    return ytmusic_service.add_songs_to_playlist(
        songs=songs,
        playlist_title=playlist_title,
        playlist_description=playlist_description,
    )


@mcp.tool()
def get_user_playlists() -> List[Dict[str, str]]:
    """
    Get all playlists in the user's YouTube Music library.

    Returns:
        A list of playlist dictionaries with id, title, and track count
    """
    return ytmusic_service.get_playlists()


@mcp.tool()
def get_playlist_songs(playlist_id_or_title: str) -> List[Dict[str, str]]:
    """
    Get all songs in a YouTube Music playlist.

    Args:
        playlist_id_or_title: The ID or title of the playlist

    Returns:
        A list of song dictionaries with title, artist, album, videoId, etc.
    """
    return ytmusic_service.get_playlist_songs(playlist_id_or_title=playlist_id_or_title)


@mcp.tool()
def remove_songs_from_playlist(
    playlist_id_or_title: str, songs: List[Dict[str, str]]
) -> Dict[str, any]:
    """
    Remove songs from a YouTube Music playlist.

    Args:
        playlist_id_or_title: The ID or title of the playlist
        songs: A list of dictionaries, each must have 'videoId' and 'setVideoId' keys
              (these come from the get_playlist_songs tool)

    Returns:
        A dictionary with status information and the number of removed songs
    """
    return ytmusic_service.remove_songs_from_playlist(
        playlist_id_or_title=playlist_id_or_title, songs=songs
    )


if __name__ == "__main__":
    mcp.run()
