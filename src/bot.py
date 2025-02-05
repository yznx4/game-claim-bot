import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

from epic import claim_epic_game
from steam import claim_steam_game

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=gemini_api_key)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Bot logged in as {client.user}')


@client.tree.command(name="claim", description="Claim a free game from Epic or Steam")
@app_commands.describe(url="Game store link")
async def claim(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        if "epicgames.com" in url:
            claim_epic_game(url)
        elif "store.steampowered.com" in url:
            claim_steam_game(url)
        else:
            await interaction.followup.send("⚠️ Unsupported link.")
            return

        await interaction.followup.send("✅ Game claimed successfully!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: Something went wrong.")
        print(f"Error: {e}")


@client.tree.command(name="curse3mo", description="curse someone by mention")
@app_commands.describe(message="Game store link")
async def curse3mo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


Guild = discord.Object(id=76530062679455151274)  # add it if you want the bot to quickly interact with your server


@client.tree.command(name="ping", description="Check if the bot is alive", guild=Guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")


GEMINI_CHANNEL_ID = 1335692045511295543  # Chanel where gemini chat


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == GEMINI_CHANNEL_ID:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash",
                                          system_instruction="you are pizza, your name is slice")
            response = model.generate_content(message.content)
            reply = response.text

            await message.channel.send(f"🤖 **wtfgpt:** {reply}")
        except Exception as e:
            await message.channel.send(f"❌ Error: Something went wrong.")
            print(f"Error: {e}")


client.run(token)
