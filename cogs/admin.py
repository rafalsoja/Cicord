from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(admin(bot))
    print("Admin Cog loaded successfully.")