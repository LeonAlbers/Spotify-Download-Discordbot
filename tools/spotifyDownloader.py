import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from mutagen.flac import FLAC
import tools.driveUploader as driveUploader

load_dotenv()

# ==== Spotify Setup ====
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

folder_id = None

# ==== Song to mp3 function ====
def download_song(track_id):
    try:
        # 1. Get track info from Spotify
        track_info = sp.track(track_id)
        track_titel = track_info['name']
        track_artist = track_info['artists'][0]['name']
        search_query = f"{track_titel} {track_artist}"
        print(f"Searching for: {search_query}")

        # 3. Download Audio from YouTube
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'songs/{track_titel} - {track_artist}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',   # Verlustfreie Qualität
                'preferredquality': '0',
            }],
            'quiet': False,  # Fortschrittsanzeige
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(f'ytsearch1:{search_query}')

        # 4. Add ID3 Tags
        audio = FLAC(f'songs/{track_titel} - {track_artist}.flac')
        audio['title'] = track_titel
        audio['artist'] = track_artist
        audio['album'] = track_info['album']['name']
        audio['date'] = track_info['album']['release_date']
        if track_info['album']['images']:
            audio['albumart'] = track_info['album']['images'][0]['url']

        audio.save()

        print(f"Downloaded and tagged: {track_titel} - {track_artist}")

        driveUploader.upload_file(f'songs/{track_titel} - {track_artist}.flac', folder_id)

    except Exception as e:
        print(f"Error fetching track info: {e}")
        return

# ==== Get track ====
def get_track(url, usr=None):
    if usr is None:
        return
    global folder_id
    if "/playlist/" in url:
        folder_id = driveUploader.create_folder(usr)
        playlist_id = url.split("playlist/")[1].split("?")[0]
        tracks = sp.playlist_tracks(playlist_id)['items']
        for item in tracks:
            track_id = item['track']['id']
            download_song(track_id)
        return driveUploader.make_folder_public(folder_id)
    elif "/album/" in url:
        folder_id = driveUploader.create_folder(usr)
        album_id = url.split("album/")[1].split("?")[0]
        tracks = sp.album_tracks(album_id)['items']
        for item in tracks:
            track_id = item['id']
            download_song(track_id)
            return driveUploader.make_folder_public(folder_id)
    elif "/track/" in url:
        folder_id = driveUploader.create_folder(usr)
        track_id = url.split("track/")[1].split("?")[0]
        download_song(track_id)
        return driveUploader.make_folder_public(folder_id)
    else:
        print("Invalid Spotify URL")
        return