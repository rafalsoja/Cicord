from discord.ext import commands

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(general(bot))
    print("Admin Cog loaded successfully.")