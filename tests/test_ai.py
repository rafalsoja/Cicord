# test/test_ai.py
import pytest, discord
from discord.ext import commands
from discord.ext import test as dpytest

from cogs.ai import AI  # upewnij się, że masz cogs/__init__.py

@pytest.fixture
def bot(event_loop, monkeypatch):
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    dpytest.configure(bot)

    # Opcjonalnie: ustaw klucz, aby uniknąć zależności od realnego configu
    monkeypatch.setattr("cogs.ai.OPENAI_API_KEY", "test-key", raising=False)

    return bot

@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    async def _noop(_):
        return None
    # Przyspiesz “animację kropek”
    monkeypatch.setattr("cogs.ai.asyncio.sleep", _noop)

@pytest.mark.asyncio
async def test_ask_success(monkeypatch, bot):
    # Mock odpowiedzi OpenAI
    class MockResponse:
        output_text = "Odpowiedź testowa AI."

    async def add_cog_and_run():
        await bot.add_cog(AI(bot))
        await dpytest.message("!ask Co to jest test?")

    # Patch cogs.ai.openai.responses.create
    def _mock_create(model, instructions, input):
        return MockResponse()

    monkeypatch.setattr("cogs.ai.openai.responses.create", _mock_create, raising=False)

    await add_cog_and_run()

    # Pierwsza wiadomość: "Processing...", druga: finalny embed z odpowiedzią
    _processing = dpytest.get_message()
    final_msg = dpytest.get_message()

    assert final_msg is not None
    assert final_msg.embeds
    assert final_msg.embeds[0].title == "Response 👌"
    assert "Odpowiedź testowa AI." in final_msg.embeds[0].description

@pytest.mark.asyncio
async def test_ask_error(monkeypatch, bot):
    # Przygotuj klasę błędu zgodną z try/except w cogu
    class MockOpenAIError(Exception):
        pass

    # Patch typu błędu
    monkeypatch.setattr("cogs.ai.openai.error.OpenAIError", MockOpenAIError, raising=False)

    # Mock, który rzuci błąd
    def _mock_create(model, instructions, input):
        raise MockOpenAIError("Błąd testowy")

    monkeypatch.setattr("cogs.ai.openai.responses.create", _mock_create, raising=False)

    await bot.add_cog(AI(bot))
    await dpytest.message("!ask Wywołaj błąd")

    # Pierwsza wiadomość: "Processing...", druga: "Error"
    _processing = dpytest.get_message()
    err_msg = dpytest.get_message()

    assert err_msg is not None
    assert err_msg.embeds
    assert err_msg.embeds[0].title == "Error"
    assert "Błąd testowy" in err_msg.embeds[0].description
