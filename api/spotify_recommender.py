import spotipy
import os
import logging
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_client():
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                scope="user-read-private user-read-email playlist-read-private"
            )
        )
        logging.info("spotify client create successfully")
        return sp
    except Exception as e:
        logging.error(f'Failed to create spotify client:{e}')
        raise

MOOD_PROFILES = {
    "happy": {
        "seed_genres": ["pop", "dance", 'kpop'],
        "target_valence": 0.85,
        "target_energy": 0.75,
        "min_tempo": 100,
    },
    "sad": {
        "seed_genres": ["acoustic", "piano"],
        "target_valence": 0.2,
        "target_energy": 0.3,
        "max_tempo": 80,
    },
    "angry": {
        "seed_genres": ["metal", "rock"],
        "target_valence": 0.3,
        "target_energy": 0.9,
        "min_tempo": 120,
    },
    "surprise": {
        "seed_genres": ["edm", "house"],
        "target_valence": 0.6,
        "target_energy": 0.8,
        "tempo": 110,
    },
    "neutral": {
        "seed_genres": ["chill", "lofi", 'r&b'],
        "target_valence": 0.5,
        "target_energy": 0.5,
    },
}


def get_recommended_tracks(mood: str):
    try:
        sp = get_spotify_client()

        profile = MOOD_PROFILES.get(mood, MOOD_PROFILES["neutral"])
        results =  sp.recommendations(
            seed_genres=profile["seed_genres"],
            target_valence=profile["target_valence"],
            target_energy=profile["target_energy"],
            limit=5,
        )

        songs=[]
        for track in results["tracks"]:
            songs.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "url": track["external_urls"]["spotify"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
            })
        logging.info(f'Found{len(songs)} track for mood:{mood}')
        return songs
    except Exception as e:
        logging.error(f'EArror fetching recommended tracks:{e}')
        return []
    
def main():
    mood = 'happy'
    logging.info(f'testing api call..')
    songs = get_recommended_tracks(mood)
    
    if not songs:
        logging.warning("No songs returned")
        return

    for i, song in enumerate(songs, 1):
        print(f"{i}. {song['name']} — {song['artist']}")
        print(f"   {song['url']}\n")


if __name__ == "__main__":
    main()