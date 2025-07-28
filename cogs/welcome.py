from string import Template

import discord
from discord.ext import commands


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, style=discord.ButtonStyle.primary):
        """A button for one role. `custom_id` is needed for persistent views."""
        super().__init__(label=role.name, style=style, custom_id=str(role.id))

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
            1274944761920225300,  # Boise
            1033893140270153749,  # Boston
            1335321808043507810,  # Buffalo
            1193739841859485758,  # Connecticut
            1088299555512131595,  # Chattanooga
            1020907447822581823,  # Chicago
            1027739489302495314,  # Cincinatti
            1020907860185579530,  # Columbus
            1210853041981497356,  # Dallas
            1024892173310767186,  # DC/MD/VA
            1324485725185511535,  # Denver
            1088299493243490354,  # Longview
            1074898462547648623,  # Houston
            1166518630545104996,  # Johnson City
            1231000334634192936,  # New Jersey
            1020906856136314901,  # NYC
            1040183449627152396,  # Milwaukee
            1262146850056704101,  # Minneapolis
            1288346931676057631,  # Philly
            1260690873520361632,  # Portland
            1210852957701279744,  # Portsmouth
            1202305868809375744,  # Providence
            1025226011832483880,  # San Francisco
            1032165548009721917,  # Seattle
            1020908145712828518,  # St. Louis
            1398325883756089395,  # Tallahassee
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
        guild = self.bot.get_guild(894703368411422790)  # The guild ID
        channel = self.bot.get_channel(
            960555939579195473
        )  # The channel ID for the role messages

        # Create two views
        first_view = discord.ui.View(timeout=None)
        second_view = discord.ui.View(timeout=None)

        # Process first 20 roles for the first view
        for count, role_id in enumerate(self.role_ids[:20]):
            role = guild.get_role(role_id)
            if role:
                first_view.add_item(
                    RoleButton(
                        role,
                        self.color_to_style[count % 4],
                    )
                )

        # Process remaining roles for the second view
        for count, role_id in enumerate(self.role_ids[20:]):
            role = guild.get_role(role_id)
            if role:
                second_view.add_item(
                    RoleButton(
                        role,
                        self.color_to_style[count % 4],
                    )
                )

        # Ensure the views are watching for interactions
        self.bot.add_view(first_view)
        self.bot.add_view(second_view)

        # Handling first message
        try:
            first_message = await channel.fetch_message(
                1052773288708948039
            )  # First button message ID
            await first_message.edit(content="Select your role:", view=first_view)
        except discord.errors.NotFound:
            await channel.send("Select your role:", view=first_view)

        # Handling second message
        try:
            second_message = await channel.fetch_message(
                1262216201543745579
            )  # Second button message ID
            await second_message.edit(content="Select your roles:", view=second_view)
        except discord.errors.NotFound:
            await channel.send("Select your roles:", view=second_view)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
