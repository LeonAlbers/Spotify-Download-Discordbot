import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from mutagen.flac import FLAC
import tools.driveUploader as driveUploader
from tools.consoleStyling import fonts

load_dotenv()

# ==== Spotify Setup ====
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

folder_id = None

# ==== Test Spotify Link ====
def test_spotify_link(url):
    if "/playlist/" in url:
        playlist_id = url.split("playlist/")[1].split("?")[0]
        try:
            sp.playlist(playlist_id)
            return True
        except Exception as e:
            print(f"{fonts.RED + fonts.BOLD}Error fetching playlist:{fonts.END} {e}")
            return False
    elif "/album/" in url:
        album_id = url.split("album/")[1].split("?")[0]
        try:
            sp.album(album_id)
            return True
        except Exception as e:
            print(f"{fonts.RED + fonts.BOLD}Error fetching album:{fonts.END} {e}")
            return False
    elif "/track/" in url:
        track_id = url.split("track/")[1].split("?")[0]
        try:
            sp.track(track_id)
            return True
        except Exception as e:
            print(f"{fonts.RED + fonts.BOLD}Error fetching track:{fonts.END} {e}")
            return False
    else:
        print(f"{fonts.RED + fonts.BOLD}Invalid Spotify URL{fonts.END}")
        return False

# ==== Song to mp3 function ====
def download_song(track_id):
    try:
        # 1. Get track info from Spotify
        track_info = sp.track(track_id)
        track_titel = track_info['name']
        track_artist = track_info['artists'][0]['name']
        search_query = f"{track_titel} {track_artist}"
        print(f"{fonts.CYAN + fonts.BOLD}Searching for:{fonts.END} {search_query}")

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
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(f'ytsearch1:{search_query}')

        # 4. Add Audio Tags
        audio = FLAC(f'songs/{track_titel} - {track_artist}.flac')
        audio['title'] = track_titel
        audio['artist'] = track_artist
        audio['album'] = track_info['album']['name']
        audio['date'] = track_info['album']['release_date']

        audio.save()

        print(f"{fonts.CYAN + fonts.BOLD}Downloaded and tagged:{fonts.END} {track_titel} - {track_artist}")

        driveUploader.upload_file(f'songs/{track_titel} - {track_artist}.flac', folder_id)

    except Exception as e:
        print(f"{fonts.RED + fonts.BOLD}Error fetching track info:{fonts.END} {e}")
        return

# ==== Get track ====
def get_track(url, usr=None):
    if usr is None:
        return
    global folder_id
    if "/playlist/" in url:
        folder_id = driveUploader.create_folder(usr)
        playlist_id = url.split("playlist/")[1].split("?")[0]
        tracks = get_playlist_tracks(playlist_id)
        for item in tracks:
            track_id = item['track']['id']
            download_song(track_id)
        return driveUploader.make_folder_public(folder_id)
    elif "/album/" in url:
        folder_id = driveUploader.create_folder(usr)
        album_id = url.split("album/")[1].split("?")[0]
        tracks = get_playlist_tracks(album_id)
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
        print(f"{fonts.RED + fonts.BOLD}Invalid Spotify URL{fonts.END}")
        return
    
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks