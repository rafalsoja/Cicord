import discord, os, asyncio
from discord.ext import commands
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

if __name__ == '__main__':
    import asyncio
    async def main():
        await load_cogs()
        await bot.start(TOKEN)
    asyncio.run(main())
