from ytmusicapi import YTMusic
from typing import List, Tuple, Dict
from auth import load_oauth_credentials, authenticate_ytmusic
from playlist import get_or_create_playlist, search_songs, add_songs_to_playlist


class YTMusicService:
    def __init__(
        self,
        client_secrets_file: str = "yt_client_secrets.json",
        oauth_file: str = "oauth.json",
    ):
        """Initialize the YTMusic service with authentication."""
        self.client_secrets_file = client_secrets_file
        self.oauth_file = oauth_file
        self.ytmusic = None

    def authenticate(self):
        """Authenticate with YouTube Music."""
        oauth_credentials = load_oauth_credentials(self.client_secrets_file)
        self.ytmusic = authenticate_ytmusic(self.oauth_file, oauth_credentials)
        return self.ytmusic

    def add_songs_to_playlist(
        self,
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
        # Make sure we're authenticated
        if self.ytmusic is None:
            self.authenticate()

        # Get or create playlist
        playlist_id = get_or_create_playlist(
            self.ytmusic, playlist_title, playlist_description
        )

        # Convert the list of song dictionaries to (title, artist) tuples
        song_tuples = [(song["title"], song["artist"]) for song in songs]

        # Search for songs
        video_ids = search_songs(self.ytmusic, song_tuples)

        # Add songs to playlist
        status = add_songs_to_playlist(
            self.ytmusic, playlist_id, video_ids, playlist_title
        )

        return {
            "playlist_id": playlist_id,
            "video_ids": video_ids,
            "status": status,
            "song_count": len(video_ids),
        }

    def get_playlists(self) -> List[Dict[str, str]]:
        """
        Get all playlists in the user's library.

        Returns:
            A list of playlist dictionaries with id, title, etc.
        """
        # Make sure we're authenticated
        if self.ytmusic is None:
            self.authenticate()

        playlists = self.ytmusic.get_library_playlists()
        return [
            {
                "id": pl.get("playlistId", ""),
                "title": pl.get("title", ""),
                "count": pl.get("count", 0),
            }
            for pl in playlists
        ]

    def get_playlist_songs(self, playlist_id_or_title: str) -> List[Dict[str, str]]:
        """
        Get all songs in a playlist.

        Args:
            playlist_id_or_title: The ID or title of the playlist

        Returns:
            A list of song dictionaries with title, artist, etc.
        """
        # Make sure we're authenticated
        if self.ytmusic is None:
            self.authenticate()

        # If a title was provided instead of an ID, find the ID
        if not playlist_id_or_title.startswith("VL"):
            playlists = self.get_playlists()
            playlist_id = next(
                (pl["id"] for pl in playlists if pl["title"] == playlist_id_or_title),
                None,
            )
            if not playlist_id:
                return []
        else:
            playlist_id = playlist_id_or_title

        # Get the songs in the playlist
        playlist = self.ytmusic.get_playlist(playlist_id, limit=1000)
        tracks = playlist.get("tracks", [])

        # Format the results
        songs = []
        for track in tracks:
            songs.append(
                {
                    "title": track.get("title", ""),
                    "artist": track.get("artists", [{}])[0].get(
                        "name", "Unknown Artist"
                    )
                    if track.get("artists")
                    else "Unknown Artist",
                    "album": track.get("album", {}).get("name", "")
                    if track.get("album")
                    else "",
                    "videoId": track.get("videoId", ""),
                    "setVideoId": track.get("setVideoId", ""),
                    "thumbnailUrl": track.get("thumbnails", [{}])[-1].get("url", "")
                    if track.get("thumbnails")
                    else "",
                }
            )

        return songs

    def remove_songs_from_playlist(
        self, playlist_id_or_title: str, songs: List[Dict[str, str]]
    ) -> Dict[str, any]:
        """
        Remove songs from a playlist.

        Args:
            playlist_id_or_title: The ID or title of the playlist
            songs: A list of dictionaries, each with 'videoId' and 'setVideoId' keys

        Returns:
            A dictionary with status information
        """
        # Make sure we're authenticated
        if self.ytmusic is None:
            self.authenticate()

        # If a title was provided instead of an ID, find the ID
        if not playlist_id_or_title.startswith("VL"):
            playlists = self.get_playlists()
            playlist_id = next(
                (pl["id"] for pl in playlists if pl["title"] == playlist_id_or_title),
                None,
            )
            if not playlist_id:
                return {"status": "Playlist not found", "removed_count": 0}
        else:
            playlist_id = playlist_id_or_title

        # Prepare the video IDs to remove
        # YTMusic API requires both videoId and setVideoId to remove a song
        video_ids_to_remove = []
        for song in songs:
            if "videoId" in song and "setVideoId" in song:
                video_ids_to_remove.append(
                    {"videoId": song["videoId"], "setVideoId": song["setVideoId"]}
                )

        if not video_ids_to_remove:
            return {"status": "No valid songs to remove", "removed_count": 0}

        # Remove the songs
        status = self.ytmusic.remove_playlist_items(playlist_id, video_ids_to_remove)

        return {
            "status": f"Removed {len(video_ids_to_remove)} songs from playlist",
            "removed_count": len(video_ids_to_remove),
            "playlist_id": playlist_id,
        }
