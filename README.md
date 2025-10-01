# Spotify-Download-Discordbot

Discord Bot for downloading songs by their Spotify link.

It takes a link to a Spotify song, playlist or album and downloads the songs as .flac files. The downloaded files will be uploaded to Google Drive and the Bot will send link to the created folder.

# How to install

1. Clone this repository.

2. Set up the [Requirements](#requirements).

3. Navigate into the directory and install the [dependencies](#dependencies). Set up the API Keys as shown in .env.example

4. Run the setup.py file in the root directory **AFTER** setting up the [Requirements](#requirements).Set the printed id in the .env.example file.

5. Rename .env.example to .env

6. To run the bot, start the bot.py file.

# Virtual Environement

A virtual environement can be used if you dont want the dependencies to be installed globaly. If you want to use this, you have to `create` it, start it and then you can run the install command (eg. `pip3 install --upgrade -r requirements.txt`).

Need to know commands:

`Create`

```bash
python3 -m venv .venv
```

`Start`

```bash
source .venv/bin/activate
```

`Stop`

```bash
deactivate
```

# Requirements

- [Python3](https://www.python.org/)
- [Discord Application](https://discord.com/developers) (Bot)
- [Spotify Application](https://developer.spotify.com/dashboard)
- [Google Drive Project](https://console.cloud.google.com)

## How to set up Discord Application

1. [Create a new Application](https://discord.com/developers)
2. Go to the Bot page and click on "Reset Token"
3. Add Token to a .env file like this: TOKEN=your_token_here
4. Enable "Message Content Intent"

## How to set up Spotify Application

1. [Create a new Application](https://developer.spotify.com/dashboard)
2. Copy Client ID and Client Secret
3. Add both like this to the .env file: SPOTIPY_CLIENT_ID=your_client_id and SPOTIPY_CLIENT_SECRET

## How to set up Google Drive Project

1. [Create new Cloud Project](https://console.cloud.google.com)
2. Go to APIs and Services
3. Activate Google Drive API
4. Go to OAuth and Clients and create a new one
5. Download the json and save it in the root directory as google_drive_secret.json
6. Go back into OAuth and then Targetgroup and add yourself as Test User.
7.

# Dependencies

- Discord.py
- Spotipy
- yt-dlp
- mutagen
- python-dotenv
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

For installing all dependencies run:

```bash
pip3 install --upgrade -r requirements.txt
```

_Some people need to replace pip3 with pip_

# Folder Structure

```bash
Spotify-Download-Discordbot/
│
├── bot.py
├── setup.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── tools/
│   ├── __init__.py
│   ├── spotifyDownloader.py
│   └── driveUploader.py
│
└── songs/
    └── README.md
```

- `tools/` - Helper modules.
- `songs/` - Temporary downloaded songs.
- `bot.py` - Main bot file.
- `setup.py` - Setup file for Setting up Google Drive.
- `requirements.txt` - Python dependencies.
- `README.md` - Project documentation.
- `LICENSE` - License file (MIT).
- `.gitignore` - Ignore-list for Git.
- `.env.example` - Template for enviroenment variables.

# License

This project is licensed under the MIT-License.
