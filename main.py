# This example requires the 'message_content' privileged intent to function.
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            activity=discord.Game(name="💻 & ☕"),
        )
        self.role_message_id = 960556131766398986  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(
                name="🔴"
            ): 1020907447822581823,  # ID of the role Chicago associated with unicode emoji '🔴'.
            discord.PartialEmoji(
                name="🟢"
            ): 1020906856136314901,  # ID of the role New York associated with unicode emoji '🟢'.
            discord.PartialEmoji(
                name="🟡"
            ): 1020907461412143135,  # ID of the role Austin associated with unicode emoji '🟡'.
            discord.PartialEmoji(
                name="🔵"
            ): 1020907860185579530,  # ID of the role Columbus associated with unicode emoji '🔵'.
            discord.PartialEmoji(
                name="⚪"
            ): 1020908145712828518,  # ID of the role St. Louis associated with unicode emoji '⚪'.
            discord.PartialEmoji(
                name="🏝️"
            ): 1021599522964639796,  # ID of the role Whidbey island associated with unicode emoji '🏝️'.
            discord.PartialEmoji(
                name="✅"
            ): 960545821189894174,  # ID of the role Verified Member associated with unicode emoji '✅'.
            discord.PartialEmoji(
                name="⚫"
            ): 1021495205641338950,  # ID of the role Virtual / Online associated with unicode emoji '⚫'.
            discord.PartialEmoji(
                name="🟣"
            ): 1024892173310767186,  # ID of the role DC/MD/VA associated with unicode emoji '⚫'.
            discord.PartialEmoji(
                name="🌽"
            ): 1027739489302495314,  # ID of the role Cincinatti associated with unicode emoji '🌽'.
            discord.PartialEmoji(
                name="☕"
            ): 1032165548009721917,  # ID of the role Seattle associated with unicode emoji '☕'.
            discord.PartialEmoji(
                name="🦞"
            ): 1033893140270153749,  # ID of the role Boston associated with unicode emoji '🦞'.
            discord.PartialEmoji(
                name="🌉"
            ): 1025226011832483880,  # ID of the role San Francisco associated with unicode emoji '🌉'.
            discord.PartialEmoji(
                name="🍑"
            ): 1036290493698555985,  # ID of the role Atlanta associated with unicode emoji '🍑'.
            discord.PartialEmoji(
                name="🏄"
            ): 1039006815599480873,  # ID of the role Ventura associated with unicode emoji '🏄'.
            discord.PartialEmoji(
                name="💡"
            ): 1042025367147401257,  # ID of the role Nova associated with unicode emoji '💡'.
            discord.PartialEmoji(
                name="🔺"
            ): 1042302822508658698,  # ID of the role Triangle associated with unicode emoji '🔺'.
            discord.PartialEmoji(
                name="🍺"
            ): 1040183449627152396,  # ID of the role Milwaukee associated with unicode emoji '🍺'.
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
            print(f"{payload.member} joined {role}")
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
            print(f"{member} left {role}")
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


bot = Bot()


@bot.command()
@commands.has_any_role("Admin", "Organizer")
async def new_chapter(ctx, chapter_name):
    organizer_role = ctx.guild.get_role(899873033592913921)
    volunteer_role = ctx.guild.get_role(993952153091702854)
    main_category = ctx.guild.get_channel(894703368411422792)

    # Create a chapter role
    chapter_role = await ctx.guild.create_role(name=chapter_name, hoist=True)
    await ctx.send(f"✅ a new role called {chapter_role.name} was created")

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

    await ctx.send(
        f"✅{chapter_role.name} now has read/write permission to the {main_category.name} category"
    )

    # create a chapter category, viewable by chapter role
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(
            read_messages=False,
            send_messages=False,
        ),
        chapter_role: discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
        ),
    }
    category = await ctx.guild.create_category(chapter_name, overwrites=overwrites)
    await ctx.send(f"✅ a new category called {category.name} was created")

    # create a general chapter text channel
    channel = await category.create_text_channel(chapter_name + "-general")
    await ctx.send(f"✅ a new text-channel called {channel.name} was created")

    # create a private chapter text channel, viewable by organizer_roles and volunteer_roles
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(
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
        chapter_name + "-private", overwrites=overwrites
    )

    await ctx.send(f"✅ a new text-channel called {channel.name} was created")


bot.run(DISCORD_TOKEN)
