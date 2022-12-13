import discord
from discord.ext import commands
from string import Template

message_content_1 = Template(
    """
**What is Code & Coffee?**
We're a community by devs for new and old devs + folks that work with them. Additionally, we're the #1 in-person community on the Meetup.com platform! Our community hosts consistent events, typically once or twice a month, where we have self-taught hackers, current/ex-FANG engineers, uni students, startup devs, fintech, bootcamp grads, and non-traditional career-switches of all ages, and many more! 

If you do anything with a text editor, you belong. Expect to meet new people, get job referrals, and meet folks hacking on cool side projects! We expect you to oblige by ${rules}.

**1. New member - Onboarding** >> START HERE <<
To view the rest of the server, click your city's colored button below - clicking these buttons will add/remove channels, please explore!
"""
)

message_content_2 = Template(
    """
2. Introduce yourself in ${intro_circle} channel

3. Say "Hi" to your local developers in the left sidebar! (optional)
"""
)


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, emoji, style=discord.ButtonStyle.primary):
        """A button for one role. `custom_id` is needed for persistent views."""
        super().__init__(
            label=role.name, style=style, custom_id=str(role.id), emoji=emoji
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
        self.role_ids = {
            1036290493698555985: discord.PartialEmoji(name="🏄"),  # Atlanta
            1020907461412143135: discord.PartialEmoji(name="🟡"),  # Austin
            1033893140270153749: discord.PartialEmoji(name="🦞"),  # Boston
            1020907447822581823: discord.PartialEmoji(name="🔴"),  # Chicago
            1027739489302495314: discord.PartialEmoji(name="🌽"),  # Cincinatti
            1020907860185579530: discord.PartialEmoji(name="🔵"),  # Columbus
            1024892173310767186: discord.PartialEmoji(name="🟣"),  # DC/MD/VA
            1020906856136314901: discord.PartialEmoji(name="🟢"),  # NYC
            1040183449627152396: discord.PartialEmoji(name="🍺"),  # Milwaukee
            1025226011832483880: discord.PartialEmoji(name="🌉"),  # San Francisco
            1032165548009721917: discord.PartialEmoji(name="☕"),  # Seattle
            1020908145712828518: discord.PartialEmoji(name="⚪"),  # St. Louis
            1042302822508658698: discord.PartialEmoji(name="🔺"),  # Triangle
            1039006815599480873: discord.PartialEmoji(name="🏄"),  # Ventura
            1021495205641338950: discord.PartialEmoji(name="⚫"),  # Virtual / Online
            1021599522964639796: discord.PartialEmoji(name="🏝️"),  # Whidbey island
        }
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
        for role_id, emoji in self.role_ids.items():
            role = guild.get_role(role_id)
            view.add_item(
                RoleButton(
                    role,
                    emoji,
                    self.color_to_style[count % 4],
                )
            )
            count += 1

        # Add the view to the bot so that it will watch for button interactions.
        self.bot.add_view(view)
        channel = self.bot.get_channel(960555939579195473)
        rules = self.bot.get_channel(960540110477222008).mention
        intro_circle = self.bot.get_channel(1020074229804302468).mention

        # 1st message
        try:
            message_1 = await channel.fetch_message(1049114511153578015)
            await message_1.edit(
                content=message_content_1.substitute(rules=rules), view=view
            )
        except discord.errors.NotFound:
            await channel.send(
                content=message_content_1.substitute(rules=rules), view=view
            )
        # 2nd message
        try:
            message_2 = await channel.fetch_message(1049144027380973623)
            await message_2.edit(
                content=message_content_2.substitute(intro_circle=intro_circle)
            )
        except discord.errors.NotFound:
            await channel.send(
                content=message_content_2.substitute(intro_circle=intro_circle)
            )
        print("welcome msg updated")


async def setup(bot):
    await bot.add_cog(Welcome(bot))
