from typing import List, Dict
from fastmcp import FastMCP
from ytmusic_service import YTMusicService

mcp = FastMCP("YouTube Music Playlist Creator 🎵")
ytmusic_service = YTMusicService()


@mcp.tool()
def create_playlist(
    title: str,
    description: str = "Created via yt-music-mcp.",
) -> Dict[str, str]:
    """
    Create a new YouTube Music playlist.

    Args:
        title: The title of the new playlist
        description: The description of the new playlist

    Returns:
        A dictionary with the playlist ID and title
    """
    return ytmusic_service.create_playlist(
        title=title,
        description=description,
    )


@mcp.tool()
def add_songs_to_yt_playlist(
    songs: List[Dict[str, str]],
    playlist_id: str,
) -> Dict[str, any]:
    """
    Add a list of songs to a YouTube Music playlist.

    Args:
        songs: A list of dictionaries, each with 'title' and 'artist' keys
        playlist_id: The ID of the playlist to add songs to

    Returns:
        A dictionary containing:
          - playlist_id: The ID of the playlist
          - added_count: Number of songs successfully added
          - failed_count: Number of songs that failed to add
          - not_found_count: Number of songs that couldn't be found
          - not_found: List of songs that couldn't be found
          - status: A human-readable status message
          - success: Whether at least one song was added successfully
    """
    return ytmusic_service.add_songs_to_playlist(
        songs=songs,
        playlist_id=playlist_id,
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
def get_playlist_songs(playlist_id: str) -> List[Dict[str, str]]:
    """
    Get all songs in a YouTube Music playlist.

    Args:
        playlist_id: The ID of the playlist

    Returns:
        A list of song dictionaries with title, artist, album, videoId, etc.
    """
    return ytmusic_service.get_playlist_songs(playlist_id=playlist_id)


@mcp.tool()
def remove_songs_from_playlist(
    playlist_id: str, songs: List[Dict[str, str]]
) -> Dict[str, any]:
    """
    Remove songs from a YouTube Music playlist.

    Args:
        playlist_id: The ID of the playlist
        songs: A list of dictionaries, each must have 'videoId' and 'setVideoId' keys
              (these come from the get_playlist_songs tool)

    Returns:
        A dictionary with status information and the number of removed songs
    """
    return ytmusic_service.remove_songs_from_playlist(
        playlist_id=playlist_id, songs=songs
    )


if __name__ == "__main__":
    mcp.run()
