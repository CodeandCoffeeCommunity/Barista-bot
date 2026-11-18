import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")


class Bot(commands.Bot):
    def __init__(self):
        # No privileged intents. This server has 10k+ members, so Discord only
        # grants them after a review. Role buttons, slash commands and
        # scheduled posts work without them.
        intents = discord.Intents.default()

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            activity=discord.Game(name="💻 & ☕"),
        )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def setup_hook(self) -> None:
        # Load cogs
        for file in os.listdir(f"./cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await bot.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")


bot = Bot()

bot.run(DISCORD_TOKEN)
