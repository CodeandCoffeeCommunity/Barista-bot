import pathlib
import re
from typing import Literal, Optional

import discord
import git
from discord import app_commands
from discord.ext import commands
from git.repo.base import Repo


neetcode = pathlib.Path("leetcode")
neetcode.mkdir(exist_ok=True)
try:
    Repo.clone_from("https://github.com/neetcode-gh/leetcode.git", neetcode)
    print("cloned repo")
except git.exc.GitCommandError:
    repo = Repo(neetcode)
    o = repo.remotes.origin
    o.pull()
    print("pulled repo")
languages = [x.name for x in neetcode.iterdir() if x.is_dir() and not x.name.startswith(".")]

class Neetcode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command()
    @app_commands.describe(
        number="the number leetcode problem you want a soluiton for",
        language=", ".join(languages),
    )
    async def leetcode(self, interaction: discord.Interaction, number: int, language: Literal[*languages]):
        """Returns the leetcode solution"""
        files = list(neetcode.glob(language+"/"+str(number)+"-*"))
        if language not in languages or len(files) == 0:
            await interaction.response.send_message(f'there are no solutions for leetcode problem #{number} in {language}')
            return
        
        with open(files[0]) as f:
            code = f.read()

        await interaction.response.send_message(f"```{language}\n{code}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(Neetcode(bot))
