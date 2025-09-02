# cogs/verify.py
import discord
from discord.ext import commands, tasks
from db import VerificationDB

class VerificationModal(discord.ui.Modal):
    def __init__(self, role: discord.Role, secret: str, question: str):
        super().__init__(title="Weryfikacja")
        self.role = role
        self.secret = secret
        self.answer = discord.ui.TextInput(label=question, placeholder="Wpisz odpowiedź", required=True)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Weryfikacja działa tylko na serwerze.", ephemeral=True)
            return

        member = interaction.user
        if self.role in member.roles:
            await interaction.response.send_message("⚠️ Już masz tę rolę.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        if self.answer.value.strip().lower() == self.secret.strip().lower():
            bot_member = interaction.guild.get_member(interaction.client.user.id)
            if not bot_member or self.role.position >= bot_member.top_role.position:
                await interaction.followup.send("❌ Bot jest niżej w hierarchii niż rola.", ephemeral=True)
                return

            try:
                await member.add_roles(self.role)
                await interaction.followup.send(f"✅ Nadano rolę: {self.role.name}", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("❌ Brak uprawnień do nadania roli.", ephemeral=True)
        else:
            await interaction.followup.send("❌ Zła odpowiedź.", ephemeral=True)

class VerificationView(discord.ui.View):
    def __init__(self, guild_id: int, db: VerificationDB):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.db = db
        button = discord.ui.Button(label="Zweryfikuj się", style=discord.ButtonStyle.green, custom_id=f"verify:{guild_id}")
        button.callback = self.on_click
        self.add_item(button)

    async def on_click(self, interaction: discord.Interaction):
        row = self.db.get_guild(interaction.guild.id) if interaction.guild else None
        if not row:
            await interaction.response.send_message("❌ Weryfikacja nie jest skonfigurowana.", ephemeral=True)
            return

        _, channel_id, _, role_id, secret, question = row
        if interaction.channel.id != channel_id:
            await interaction.response.send_message("❌ Weryfikacja tylko na wyznaczonym kanale.", ephemeral=True)
            return

        role = interaction.guild.get_role(role_id)
        if not role:
            await interaction.response.send_message("❌ Rola nie istnieje.", ephemeral=True)
            return

        await interaction.response.send_modal(VerificationModal(role, secret, question))

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = VerificationDB()
        self._restore_views.start()

    def cog_unload(self):
        self._restore_views.cancel()

    @tasks.loop(count=1)
    async def _restore_views(self):
        await self.bot.wait_until_ready()
        for guild_id, _, _, _, _, _ in self.db.all_guilds():
            self.bot.add_view(VerificationView(guild_id, self.db))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setupverify(self, ctx, role: discord.Role, secret: str, *, question: str = "Podaj hasło"):
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        if role.position >= bot_member.top_role.position:
            await ctx.send("❌ Bot jest niżej w hierarchii niż rola.")
            return

        view = VerificationView(ctx.guild.id, self.db)
        embed = discord.Embed(title="🔑 Weryfikacja", description="Kliknij przycisk i podaj hasło.", color=discord.Color.green())
        msg = await ctx.send(embed=embed, view=view)

        self.db.upsert_guild(ctx.guild.id, ctx.channel.id, msg.id, role.id, secret, question)
        self.bot.add_view(view)
        await ctx.send("✅ Weryfikacja skonfigurowana.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setverifyquestion(self, ctx, *, question: str):
        row = self.db.get_guild(ctx.guild.id)
        if not row:
            await ctx.send("❌ Weryfikacja nie jest skonfigurowana.")
            return
        guild_id, channel_id, message_id, role_id, secret, _ = row
        self.db.upsert_guild(guild_id, channel_id, message_id, role_id, secret, question)
        await ctx.send("✅ Zmieniono pytanie weryfikacyjne.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removeverify(self, ctx):
        row = self.db.get_guild(ctx.guild.id)
        if not row:
            await ctx.send("ℹ️ Brak konfiguracji.")
            return
        _, channel_id, message_id, _, _, _ = row
        self.db.delete_guild(ctx.guild.id)

        channel = ctx.guild.get_channel(channel_id)
        if channel:
            try:
                msg = await channel.fetch_message(message_id)
                await msg.delete()
            except Exception:
                pass

        await ctx.send("🧹 Usunięto konfigurację.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot))
    print("✅ Verify Cog loaded successfully.")
