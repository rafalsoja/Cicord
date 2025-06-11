import pytest, discord, warnings
from discord.ext import commands
from cogs.general import General
from unittest.mock import PropertyMock, patch

warnings.filterwarnings("ignore", category=DeprecationWarning)

class DummyCtx:
    def __init__(self):
        self.sent = None

    async def send(self, embed=None, content=None):
        self.sent = embed or content

@pytest.mark.asyncio
async def test_cogs_command_lists_other_cogs():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    with patch.object(type(bot), "cogs", new_callable=PropertyMock) as mock_cogs:
        mock_cogs.return_value = {
            "music": object(),
            "ai": object(),
            "general": object()
        }

        cog = General(bot)
        ctx = DummyCtx()

        # Wywołujemy faktyczną funkcję przypisaną do komendy
        await cog.cogs.callback(cog, ctx)

        assert ctx.sent.title == "Activated Cogs"
        assert "music" in ctx.sent.description
        assert "ai" in ctx.sent.description
        assert "general" not in ctx.sent.description
