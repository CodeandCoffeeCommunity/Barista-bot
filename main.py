# This example requires the 'message_content' privileged intent to function.
import os

import discord
from discord.ext import commands

from meetup_rest_api import fetch_meetup_events_detail

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

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"), intents=intents
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

        # Create the view containing our dropdown
        view = DropdownView(scheduled_events)

        # Sending a message containing our view
        await ctx.send("Pick your event(s):", view=view)
    else:
        await ctx.send(
            "Pull meetup.com events over to discord\n\nUsage: !event <INSERT MEETUP.COM GROUP URL>"
        )


bot.run(DISCORD_TOKEN)
