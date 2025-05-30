from discord.ext import commands
import discord, os, sys, openai, asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import OPENAI_API_KEY
from openai import OpenAI

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = OPENAI_API_KEY

    @commands.command(name='ask')
    async def ask(self, ctx, *, question: str):
        embed = discord.Embed(
            title="🤔 Processing your question...",
            description="Wait a second, I'm thinking about your question.",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)
        dots = ["", ".", "..", "..."]
        for i in range(8):
            embed.description = f"Thinking{dots[i % 4]}"
            await message.edit(embed=embed)
            await asyncio.sleep(0.5)
        try:
            response = openai.responses.create(
                model="gpt-4o",
                instructions="You are a helpful assistant. Answer the question to the best of your ability.",
                input=question
            )
            #answer = response['choices'][0]['message']['content']
            await message.delete()
            embed = discord.Embed(
                title="Response 👌",
                description=response.output_text,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except openai.error.OpenAIError as e:
            await message.delete()
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while processing your request: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AI(bot))
    print("AI Cog loaded successfully.")