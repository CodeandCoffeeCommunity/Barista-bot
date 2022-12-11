# This example requires the 'message_content' privileged intent to function.
import os

import discord
from string import Template
from discord.ext import commands
from discord.ext import tasks
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

import datetime

load_dotenv()

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")

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


# This is the list of role IDs that will be added as buttons.
role_ids = [
    (1036290493698555985, "🏄"),  # Atlanta
    (1020907461412143135, "🟡"),  # Austin
    (1033893140270153749, "🦞"),  # Boston
    (1020907447822581823, "🔴"),  # Chicago
    (1027739489302495314, "🌽"),  # Cincinatti
    (1020907860185579530, "🔵"),  # Columbus
    (1024892173310767186, "🟣"),  # DC/MD/VA
    (1020906856136314901, "🟢"),  # NYC
    (1040183449627152396, "🍺"),  # Milwaukee
    (1025226011832483880, "🌉"),  # San Francisco
    (1032165548009721917, "☕"),  # Seattle
    (1020908145712828518, "⚪"),  # St. Louis
    (1042302822508658698, "🔺"),  # Triangle
    (1039006815599480873, "🏄"),  # Ventura
    (1021495205641338950, "⚫"),  # Virtual / Online
    (1021599522964639796, "🏝️"),  # Whidbey island
]


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


class LinkButton(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()

        self.add_item(discord.ui.Button(label=label, url=url))


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
        self.color_to_style = {
            0: discord.ButtonStyle.danger,  # red
            1: discord.ButtonStyle.blurple,  # purple
            2: discord.ButtonStyle.success,  # green
            3: discord.ButtonStyle.secondary,  # gray
        }

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        # We recreate the view as we did in the /post command.
        view = discord.ui.View(timeout=None)
        # Make sure to set the guild ID here to whatever server you want the buttons in!
        guild = self.get_guild(894703368411422790)
        count = 0
        for role_id, emoji in role_ids:
            role = guild.get_role(role_id)
            view.add_item(
                RoleButton(
                    role,
                    discord.PartialEmoji(name=emoji),
                    self.color_to_style[count % 4],
                )
            )
            count += 1

        # Add the view to the bot so that it will watch for button interactions.
        self.add_view(view)
        channel = self.get_channel(960555939579195473)
        rules = self.get_channel(960540110477222008).mention
        intro_circle = self.get_channel(1020074229804302468).mention

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

    async def setup_hook(self) -> None:
        # Load cogs
        for file in os.listdir(f"./cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await bot.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")

        # start the task to run in the background
        self.monday_office_hour_reminder.start()

    @tasks.loop(
        time=datetime.time(hour=19, minute=30, tzinfo=ZoneInfo("America/New_York"))
    )
    async def monday_office_hour_reminder(self):
        now = datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        if now.isoweekday() != 2:
            return

        channel = self.get_channel(980353246361169950)
        office_hour_msg = """
@here **Happening now**

Staff Office hours - Weekly  

Casual office hours. Come chat in the Google Meet with the different chapters. Ask questions, get help, meet each other, etc. fully up to you!
"""
        await channel.send(
            content=office_hour_msg,
            view=LinkButton("Google meet", "https://meet.google.com/xnq-fdtk-ibh"),
        )


bot = Bot()

bot.run(DISCORD_TOKEN)
