from ytmusicapi import YTMusic
from typing import List, Tuple, Dict, Any


def create_playlist(ytmusic: YTMusic, title: str, description: str) -> str:
    """Create a new playlist and return its ID."""
    playlist_id = ytmusic.create_playlist(title, description)
    return playlist_id


def search_songs(ytmusic: YTMusic, songs: List[Tuple[str, str]]) -> Dict[str, Any]:
    """
    Search for songs and return their video IDs along with detailed results.

    Returns:
        Dictionary containing:
        - video_ids: List of found video IDs
        - not_found: List of songs that weren't found
        - results: List of search results with song details
    """
    video_ids = []
    not_found = []
    results = []

    for title, artist in songs:
        search_query = f"{title} {artist}"
        result = ytmusic.search(search_query, filter="songs", limit=1)

        if result and len(result) > 0:
            video_id = result[0]["videoId"]
            video_ids.append(video_id)
            results.append(
                {
                    "query": search_query,
                    "title": title,
                    "artist": artist,
                    "found": True,
                    "video_id": video_id,
                    "result_title": result[0].get("title", ""),
                    "result_artist": result[0]
                    .get("artists", [{}])[0]
                    .get("name", "Unknown")
                    if result[0].get("artists")
                    else "Unknown",
                }
            )
        else:
            not_found.append(f"{title} by {artist}")
            results.append(
                {
                    "query": search_query,
                    "title": title,
                    "artist": artist,
                    "found": False,
                }
            )

    return {"video_ids": video_ids, "not_found": not_found, "results": results}


def add_songs_to_playlist(
    ytmusic: YTMusic, playlist_id: str, search_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add songs to the specified playlist one by one and return detailed status.

    Args:
        ytmusic: Authenticated YTMusic instance
        playlist_id: ID of the playlist to add songs to
        search_results: Results from search_songs function

    Returns:
        Dictionary with detailed status about successful and failed additions
    """
    video_ids = search_results["video_ids"]
    not_found = search_results["not_found"]

    if not video_ids:
        return {
            "success": False,
            "added_count": 0,
            "failed_count": 0,
            "not_found_count": len(not_found),
            "not_found": not_found,
            "message": "No matches found, no songs were added to the playlist.",
        }

    # Get playlist title
    try:
        playlist_info = ytmusic.get_playlist(playlist_id, limit=1)
        playlist_title = playlist_info.get("title", playlist_id)
    except:
        playlist_title = playlist_id

    # Add songs one by one
    added = []
    failed = []

    for video_id in video_ids:
        try:
            status = ytmusic.add_playlist_items(playlist_id, [video_id])
            if status.get("status") == "STATUS_SUCCEEDED":
                added.append(video_id)
            else:
                failed.append(video_id)
        except Exception as e:
            failed.append(video_id)

    # Generate summary message
    messages = []
    if added:
        messages.append(f"Added {len(added)} track(s) to '{playlist_title}'")
    if failed:
        messages.append(f"Failed to add {len(failed)} track(s)")
    if not_found:
        messages.append(f"Could not find {len(not_found)} track(s)")

    summary = ". ".join(messages) + "."

    return {
        "success": len(added) > 0,
        "added_count": len(added),
        "failed_count": len(failed),
        "not_found_count": len(not_found),
        "added": added,
        "failed": failed,
        "not_found": not_found,
        "playlist_id": playlist_id,
        "playlist_title": playlist_title,
        "message": summary,
    }
