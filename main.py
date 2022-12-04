# This example requires the 'message_content' privileged intent to function.
import os

import discord
from string import Template
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("BARISTA_TOKEN")

message_content = Template("""
Welcome to **Code & Coffee**!
We're a community of developers looking to grow and make new friends.

**What is Code & Coffee?**
We are the #1 in-person community on the Meetup.com platform. Our community hosts events typically twice a month, where we have self-taught hackers, current/ex FANG engineers, uni students, startup devs, fintech, bootcamp grads, and non-traditional career-switches of all ages, and more! If you do anything with an IDE you belong. Expect to meet new people, get job referrals, and see people hacking on cool side projects! We expect you to oblige by the Code of Conduct conveniently in ${rules}.

**1. New member - Onboarding >> START HERE<<**
To view the rest of the server, click your city's colored button below:

👈 You'll see your city's Discord channel on the left sidebar. 

**2. Introduce yourself in ${intro_circle} channel** 

**3. Say "Hi" to your local developers in the left sidebar! (optional)**

Don't have a local chapter? Message @Steve Chen we have a "just add human ✨ " C&C starter kit ready for you, a support network of chapter leaders, and resources that'll guide you through it. 
""")

# This is the list of role IDs that will be added as buttons.
role_ids = [
    (1020907447822581823, discord.ButtonStyle.primary),  # Chicago
    (1020906856136314901, discord.ButtonStyle.gray),  # NYC
    (1020907461412143135, discord.ButtonStyle.danger),  # Austin
    (1020907860185579530, discord.ButtonStyle.green),  # Columbus
    (1020908145712828518, discord.ButtonStyle.blurple),  # St. Louis
    (1021599522964639796, discord.ButtonStyle.red),  # Whidbey island
    (1021495205641338950, discord.ButtonStyle.success),  # Virtual / Online
    (1024892173310767186, discord.ButtonStyle.gray),  # DC/MD/VA
    (1027739489302495314, discord.ButtonStyle.success),  # Cincinatti
    (1032165548009721917, discord.ButtonStyle.green),  # Seattle
    (1033893140270153749, discord.ButtonStyle.primary),  # Boston
    (1025226011832483880, discord.ButtonStyle.secondary),  # San Francisco
    (1036290493698555985, discord.ButtonStyle.danger),  # Atlanta
    (1039006815599480873, discord.ButtonStyle.success),  # Ventura
    (1042302822508658698, discord.ButtonStyle.danger),  # Triangle
    (1040183449627152396, discord.ButtonStyle.success),  # Milwaukee
]


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, style=discord.ButtonStyle.primary):
        """A button for one role. `custom_id` is needed for persistent views."""
        super().__init__(
            label=role.name,
            style=style,
            custom_id=str(role.id),
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
        else:
            # Otherwise, take the role away from the user.
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ The {role.mention} role has been taken from you!",
                ephemeral=True,
            )


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
        # We recreate the view as we did in the /post command.
        view = discord.ui.View(timeout=None)
        # Make sure to set the guild ID here to whatever server you want the buttons in!
        guild = self.get_guild(894703368411422790)
        for role_id, style in role_ids:
            role = guild.get_role(role_id)
            view.add_item(RoleButton(role, style))

        # Add the view to the bot so that it will watch for button interactions.
        self.add_view(view)
        channel = self.get_channel(960555939579195473)
        link_str_data = {
                "rules": self.get_channel(960540110477222008).mention,
                "intro_circle": self.get_channel(1020074229804302468).mention,
                }
        # message_content = "Click a button to assign yourself a city role"
        try:
            message = await channel.fetch_message(1049035230880743515)
            await message.edit(content=message_content.substitute(link_str_data), view=view)
        except discord.errors.NotFound:
            await channel.send(content=message_content.substitute(link_str_data), view=view)

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
