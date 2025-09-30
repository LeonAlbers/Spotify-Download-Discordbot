import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('Ctrl+C to quit')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

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

bot.run(TOKEN)