import os

import discord

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
