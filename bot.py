import discord
from discord.ext import commands

from tools.consoleStyling import fonts

import asyncio

drive_lock = asyncio.Lock()

from tools.spotifyDownloader import get_track, download_song, test_spotify_link

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'{fonts.CYAN + fonts.BOLD}Logged in as {bot.user}{fonts.END}')
    print(f'{fonts.MAGENTA + fonts.BOLD}Ctrl+C to quit{fonts.END}')
    try:
        synced = await bot.tree.sync()
        print(f'{fonts.CYAN + fonts.BOLD}Synced {len(synced)} command(s){fonts.END}')
    except Exception as e:
        print(f'{fonts.RED + fonts.BOLD}Error syncing commands:{fonts.END} {e}')

# Ignore all messages so no errors in console
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    return

@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@bot.tree.command(name="download", description="Download a song, album or playlist from Spotify")
async def download(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)

    if test_spotify_link(url) == False:
        await interaction.followup.send("❌ Invalid Spotify URL. Please provide a valid track, album, or playlist link.")
        return

    await interaction.followup.send(f"⏳ Starting download for: {url}")

    try:
        async with drive_lock:
            publicLink = await asyncio.to_thread(get_track, url, usr=interaction.user.name)

        if publicLink:
            await interaction.followup.send(f"✅ Done!\nHere is your link: {publicLink}")
        else:
            await interaction.followup.send("⚠️ An error occured during the creation of the public link.")

    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred: {e}")
        print(f"{fonts.RED + fonts.BOLD}Error during download:{fonts.END} {e}")

bot.run(TOKEN)