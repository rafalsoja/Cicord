import discord
from discord.ext import commands
import psutil
import platform
from datetime import datetime

class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(name="stats", help="Shows the resource usage and system information of the bot.")
    async def show_stats(self, ctx):
        # Collecting memory usage information
        mem = self.process.memory_full_info()
        ram_used = mem.rss / 1024 ** 2  # value in MB
        ram_total = psutil.virtual_memory().total / 1024 ** 2  # same here
        ram_percent = self.process.memory_percent()

        # Collecting CPU usage information
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        # System and Python information
        system_info = platform.system()
        python_version = platform.python_version()
        discord_version = discord.__version__

        # Bot uptime
        uptime = datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        # Creating the embed message
        embed = discord.Embed(
            title="📊 Cicord stats",
            color=discord.Color.blue()
        )

        embed.add_field(name="🖥️ RAM usage", value=f"{ram_used:.2f} MB / {ram_total:.2f} MB ({ram_percent:.2f}%)", inline=False)
        embed.add_field(name="⚡ CPU usage", value=f"{cpu_usage:.2f}%", inline=False)
        embed.add_field(name="⏱️ Uptime", value=f"{days}d {hours}h {minutes}m {seconds}s", inline=False)
        embed.add_field(name="📌 System", value=system_info, inline=True)
        embed.add_field(name="🐍 Python", value=python_version, inline=True)
        embed.add_field(name="🔌 Discord.py", value=discord_version, inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    # Saving the start time when the bot is loaded
    bot.start_time = datetime.now()
    await bot.add_cog(StatsCog(bot))
    print("Stats Cog loaded successfully.")