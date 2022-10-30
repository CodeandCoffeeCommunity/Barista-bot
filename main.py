# This example requires the 'message_content' privileged intent to function.
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from meetup_rest_api import fetch_meetup_events_detail

load_dotenv()

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")

# Defines a custom Select containing events from meetup.com
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self, scheduled_events: dict):

        # Set the options that will be presented inside the dropdown
        self.scheduled_events = scheduled_events
        options = []
        for event_id, event in self.scheduled_events.items():
            options.append(
                discord.SelectOption(
                    value=event_id,
                    label=event["name"],
                    description=event["start_time"].strftime("%m/%d/%Y"),
                )
            )

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Select events you wish to import",
            min_values=1,
            max_values=len(self.scheduled_events),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        guild = interaction.guild
        for event_id in self.values:
            event = self.scheduled_events[event_id]
            await guild.create_scheduled_event(**event)

        await interaction.response.send_message(
            f'{len(self.values)} event{"s" if len(self.values) > 1 else ""} created'
        )


class DropdownView(discord.ui.View):
    def __init__(self, scheduled_events: dict):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(scheduled_events))


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
async def event(ctx, chapter=None):
    """Sends a message with our dropdown containing colours"""

    if chapter is not None:
        scheduled_events = fetch_meetup_events_detail(chapter)
        if scheduled_events:

            # Create the view containing our dropdown
            view = DropdownView(scheduled_events)

            # Sending a message containing our view
            await ctx.send("Pick your event(s):", view=view)
        else:
            await ctx.send(f"No upcoming events for {chapter}")
    else:
        await ctx.send(
            "Pull meetup.com events over to discord\n\nUsage: !event <INSERT MEETUP.COM GROUP URL>"
        )


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
    await main_category.edit(overwrites=overwrites, sync_permissions=True)
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
