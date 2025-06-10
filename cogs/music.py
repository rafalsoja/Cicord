import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None

    async def create_music_embed(self, title, description, color=0x00ff00):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        if self.current and hasattr(self.current, 'thumbnail') and self.current.thumbnail:
            embed.set_thumbnail(url=self.current.thumbnail)
        embed.set_footer(text="Cicord Music Player")
        return embed

    @commands.command(name='play', help='Plays a music from a URL or search term')
    async def play(self, ctx, *, url):
        if not ctx.author.voice:
            embed = await self.create_music_embed(
                "❌ Error",
                "You're not connected to a voice channel!",
                color=0xff0000
            )
            return await ctx.send(embed=embed)
            
        voice_channel = ctx.author.voice.channel
        
        try:
            if ctx.voice_client is None:
                await voice_channel.connect()
            elif ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
        except Exception as e:
            embed = await self.create_music_embed(
                "❌ Error",
                f"Failed to connect: {e}",
                color=0xff0000
            )
            return await ctx.send(embed=embed)
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            self.current = player
            
            embed = await self.create_music_embed(
                "🎵 Now playing: ",
                f"[{player.title}]({url})",
                color=0x00ff00
            )
            if player.thumbnail:
                embed.set_image(url=player.thumbnail)
            
        await ctx.send(embed=embed)

    @commands.command(name='stop', help='Zatrzymuje odtwarzanie i wychodzi z kanału')
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            embed = await self.create_music_embed(
                "⏹️ Stop",
                "Music player stopped and disconnected.",
                color=0xff9900
            )
            await ctx.send(embed=embed)
        else:
            embed = await self.create_music_embed(
                "❌ Error",
                "I'm not playing anything! :triumph:",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='pause', help='Pauses the currently playing music')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = await self.create_music_embed(
                "⏸️ Paused",
                f"Pause: {self.current.title}",
                color=0xffff00
            )
            await ctx.send(embed=embed)
        else:
            embed = await self.create_music_embed(
                "❌ Error",
                "Nothing is playing!",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='resume', help='Resumes paused music')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = await self.create_music_embed(
                "▶️ Resume",
                f"Resuming: {self.current.title}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            embed = await self.create_music_embed(
                "❌ Error",
                "Music player isn't paused!",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='volume', help='Changes volume (0-100)')
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None or ctx.voice_client.source is None:
            embed = await self.create_music_embed(
                "❌ Error",
                "Nothing is playing or you're not on a voice channel!",
                color=0xff0000
            )
            return await ctx.send(embed=embed)
            
        if 0 < volume <= 100:
            ctx.voice_client.source.volume = volume / 100
            embed = await self.create_music_embed(
                "🔊 Volume",
                f"Volume set on {volume}%",
                color=0x0099ff
            )
            await ctx.send(embed=embed)
        else:
            embed = await self.create_music_embed(
                "❌ Error",
                "Enter value between 0 and 100!",
                color=0xff0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
    print("Music Cog loaded successfully.")