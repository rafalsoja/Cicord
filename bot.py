import discord
from discord.ext import commands
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

if __name__ == '__main__':
    bot.run(TOKEN)