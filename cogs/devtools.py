import logging
import typing

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

_logger = logging.getLogger(__name__)


class DevTools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: typing.Optional[typing.Literal["~", "*", "^"]] = None,
    ) -> None:
        """Syncs command tree.
        Parameters
        -----------
        guilds: list[int]
            The guilds to sync to
        spec: str
            The spec to sync.
            ~ -> Current Guild
            * -> Globals to current guild
            ^ -> Clear globals copied to current guild.
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.
        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.
        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(description=message, color=0x9C84EF)
        await context.send(embed=embed)

    async def on_ready(self):
        print("ready from within DevTools cog")


async def setup(bot):
    _logger.info("Loading DevTools cog")
    await bot.add_cog(DevTools(bot))


async def teardown(_):
    _logger.info("Extension: Unloading DevTools")
