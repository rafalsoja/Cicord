import discord
from discord.ext import commands

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='stats')
    async def stats(self, ctx):
        embed = discord.Embed(
            title="Bot Statistics",
            description="Here are the current statistics of the bot.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(set(self.bot.get_all_members())), inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(general(bot))
    print("General Cog loaded successfully.")