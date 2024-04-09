import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Chapters(commands.Cog, name="chapters"):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_any_role("Admin", "Organizer")
    @commands.hybrid_command(
        name="new_chapter",
        description="The bot will create a new chapter.",
    )
    @app_commands.describe(city="The city the bot should create")
    async def new_chapter(self, context: Context, *, city: str) -> None:
        """
        The bot will say anything you want.
        :param context: The hybrid command context.
        :param city: The city that should be repeated by the bot.
        """

        organizer_role = context.guild.get_role(899873033592913921)
        volunteer_role = context.guild.get_role(993952153091702854)
        main_category = context.guild.get_channel(894703368411422792)

        # Create a chapter role
        chapter_role = await context.guild.create_role(name=city, hoist=True, mentionable=True)
        await context.send(f"✅ a new role called {chapter_role.name} was created")

        # Give chapter role permission to read/write in main category
        overwrites = main_category.overwrites
        overwrites[chapter_role] = discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
        )
        await main_category.edit(overwrites=overwrites)

        # Apply changes to all channels in main
        for i in main_category.channels:
            await i.edit(sync_permissions=True)

        await context.send(
            f"✅{chapter_role.name} now has read/write permission to the {main_category.name} category"
        )

        # create a chapter category, viewable by chapter role
        overwrites = {
            context.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            chapter_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
        }
        category = await context.guild.create_category(city, overwrites=overwrites)
        await context.send(f"✅ a new category called {category.name} was created")

        # create a general chapter text channel
        channel = await category.create_text_channel("general")
        await context.send(f"✅ a new text-channel called {channel.name} was created")

        # create a private chapter text channel, viewable by organizer_roles and volunteer_roles
        overwrites = {
            context.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
            ),
            organizer_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
            volunteer_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
        }
        channel = await category.create_text_channel(
            "staff", overwrites=overwrites
        )

        await context.send(f"✅ a new text-channel called {channel.name} was created")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Chapters(bot))
