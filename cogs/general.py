import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='cogs')
    async def cogs(self, ctx):
        """
        Lists all activated cogs except the 'general' cog.
        This command is useful for checking which cogs are currently active in the bot.        
        """
        activated_cogs = [cog for cog in self.bot.cogs if cog != "general"]
        if not activated_cogs:
            embed = discord.Embed(title="Activated Cogs", description="No cogs are currently activated.", color=discord.Color.red())
            return await ctx.send(embed=embed)
        embed = discord.Embed(title="Activated Cogs", description="\n".join(activated_cogs), color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='enablecog')
    async def enable_cog(self, ctx, cog_name: str): 
        """
        Enable a cog by name. The cog must be in the 'cogs' directory.
        Inside config.py, you can specify which cogs to load at startup.
        Example: !enablecog admin
        """
        full_name = f'cogs.{cog_name}'
        if full_name in self.bot.extensions:
            embed = discord.Embed(
                title="Cog Already Enabled",
                description=f"The cog `{cog_name}` is already enabled.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        try:
            await self.bot.load_extension(full_name)
            embed = discord.Embed(
                title="Cog Enabled",
                description=f"The cog `{cog_name}` has been enabled.",
                color=discord.Color.green()
            )
        except Exception as e:
            embed = discord.Embed(
                title="Error Enabling Cog",
                description=f"Failed to enable `{cog_name}`: {type(e).__name__} - {e}",
                color=discord.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command(name='disablecog')
    async def disable_cog(self, ctx, cog_name: str):
        """
        Disables and unloads a cog by name.
        The cog must be in the 'cogs' directory and currently enabled.
        Example: !disablecog admin
        
        """
        full_name = f'cogs.{cog_name}'
        if full_name not in self.bot.extensions:
            embed = discord.Embed(
                title="Cog Not Found",
                description=f"The cog `{cog_name}` is not currently enabled.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        try:
            await self.bot.unload_extension(full_name)
            embed = discord.Embed(
                title="Cog Disabled",
                description=f"The cog `{cog_name}` has been disabled.",
                color=discord.Color.green()
            )
        except Exception as e:
            embed = discord.Embed(
                title="Error Disabling Cog",
                description=f"Failed to disable `{cog_name}`: {type(e).__name__} - {e}",
                color=discord.Color.red()
            )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
    print("General Cog loaded successfully.")