from string import Template

import discord
from discord.ext import commands


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, style=discord.ButtonStyle.primary):
        """A button for one role. `custom_id` is needed for persistent views."""
        super().__init__(
            label=role.name, style=style, custom_id=str(role.id)
        )

    async def callback(self, interaction: discord.Interaction):
        """
        This function will be called any time a user clicks on this button.
        Parameters
        ----------
        interaction: :class:`discord.Interaction`
            The interaction object that was created when a user clicks on a button.
        """
        # Get the user who clicked the button.
        user = interaction.user
        # Get the role this button is for (stored in the custom ID).
        role = interaction.guild.get_role(int(self.custom_id))

        if role is None:
            # If the specified role does not exist, return nothing.
            # Error handling could be done here.
            return

        # Add the role and send a response to the user ephemerally (hidden to other users).
        if role not in user.roles:
            # Give the user the role if they don't already have it.
            await user.add_roles(role)
            await interaction.response.send_message(
                f"🎉 You have been given the role {role.mention}!",
                ephemeral=True,
            )
            print(f"{user} joined {role}")
        else:
            # Otherwise, take the role away from the user.
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ The {role.mention} role has been taken from you!",
                ephemeral=True,
            )
            print(f"{user} left {role}")


class Welcome(commands.Cog, name="welcome"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.welcome_msg())

        # This is the list of role IDs that will be added as buttons.
        self.role_ids = [
            1036290493698555985,  # Atlanta
            1020907461412143135,  # Austin
            1033893140270153749,  # Boston
            1172386669081669683,  # Committed Coders Program
            1088299555512131595,  # Chattanooga
            1020907447822581823,  # Chicago
            1027739489302495314,  # Cincinatti
            1020907860185579530,  # Columbus
            1024892173310767186,  # DC/MD/VA
            1088299493243490354,  # Longview
            1074898462547648623,  # Houston
            1166518630545104996,  # Johnson City
            1020906856136314901,  # NYC
            1040183449627152396,  # Milwaukee
            1025226011832483880,  # San Francisco
            1032165548009721917,  # Seattle
            1020908145712828518,  # St. Louis
            1042302822508658698,  # Triangle
            1039006815599480873,  # Ventura
            1021495205641338950,  # Virtual / Online
            1021599522964639796,  # Whidbey island
        ]
        self.color_to_style = {
            0: discord.ButtonStyle.danger,  # red
            1: discord.ButtonStyle.blurple,  # purple
            2: discord.ButtonStyle.success,  # green
            3: discord.ButtonStyle.secondary,  # gray
        }

    async def welcome_msg(self) -> None:

        await self.bot.wait_until_ready()
        # We recreate the view as we did in the /post command.
        view = discord.ui.View(timeout=None)
        # Make sure to set the guild ID here to whatever server you want the buttons in!
        guild = self.bot.get_guild(894703368411422790)
        count = 0
        for role_id in self.role_ids:
            role = guild.get_role(role_id)
            view.add_item(
                RoleButton(
                    role,
                    self.color_to_style[count % 4],
                )
            )
            count += 1

        # Add the view to the bot so that it will watch for button interactions.
        self.bot.add_view(view)
        channel = self.bot.get_channel(960555939579195473)

        # button message
        try:
            message_button = await channel.fetch_message(1052773288708948039) # Button msg in welcome channel
            await message_button.edit(view=view)
        except discord.errors.NotFound:
            admin_channel = self.bot.get_channel(1020936089361448982)
            welcome = self.bot.get_channel(960555939579195473).mention
            await admin_channel.send(
                content=f"I'm having trouble with the buttons in the {welcome} channel"
            )


async def setup(bot):
    await bot.add_cog(Welcome(bot))
