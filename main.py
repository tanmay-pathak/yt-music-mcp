from ytmusicapi import YTMusic, OAuthCredentials


def main():
    SONGS = [
        ("Rolling in the Deep", "Adele"),
        ("Bohemian Rhapsody", "Queen"),
    ]

    PLAYLIST_TITLE = "AI Playlist"
    PLAYLIST_DESCRIPTION = "Songs added via yt-music-mcp."

    # Read client ID and secret from the client secrets file
    import json
    with open("yt_client_secrets.json", "r") as f:
        client_secrets = json.load(f)
        
    # Create OAuth credentials with client_id and client_secret from the nested structure
    creds = OAuthCredentials(
        client_id=client_secrets["installed"]["client_id"],
        client_secret=client_secrets["installed"]["client_secret"]
    )
    yt = YTMusic("oauth.json", oauth_credentials=creds)

    # create or fetch the playlist
    playlist_id = next(
        (
            pl["playlistId"]
            for pl in yt.get_library_playlists()
            if pl["title"] == PLAYLIST_TITLE
        ),
        yt.create_playlist(PLAYLIST_TITLE, PLAYLIST_DESCRIPTION),
    )

    # search & collect video IDs
    video_ids = []
    for title, artist in SONGS:
        result = yt.search(f"{title} {artist}", filter="songs", limit=1)
        if result:
            video_ids.append(result[0]["videoId"])

    # add to playlist
    if video_ids:
        yt.add_playlist_items(playlist_id, video_ids)
        print(f"Added {len(video_ids)} tracks to '{PLAYLIST_TITLE}'.")
    else:
        print("No matches found.")


if __name__ == "__main__":
    main()
