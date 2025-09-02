from discord.ext import commands
import discord, os, sys, openai, asyncio
from config import OPENAI_API_KEY
from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = OPENAI_API_KEY

    @commands.command(name='ask')
    async def ask(self, ctx, *, question: str):
        """Ask the AI a question.
        This command asks the AI a question and displays the response back to the user.
        The AI is a helpful assistant and will answer the question to the best of its ability.
        If an error occurs while processing the request, an error message will be displayed.
        """
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
    print("✅ AI Cog loaded successfully.")