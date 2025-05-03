from ytmusicapi import YTMusic
from typing import List, Tuple


def create_playlist(ytmusic: YTMusic, title: str, description: str) -> str:
    """Create a new playlist and return its ID."""
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
