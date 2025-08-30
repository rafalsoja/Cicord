import os
from dotenv import load_dotenv
load_dotenv()

# your Discord bot token and OpenAI API key
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# command prefix for the bot
PREFIX = "!"

# list of activated cogs to load
# these cogs will be loaded when the bot starts
ACTIVATED_COGS = [
    "admin",
    "ai",
    "general",
    "music",
    "stats",
    "verify"]