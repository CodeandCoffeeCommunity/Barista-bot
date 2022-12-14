import discord
import datetime
from discord.ext import commands
from discord.ext import tasks
from zoneinfo import ZoneInfo


class LinkButton(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()

        self.add_item(discord.ui.Button(label=label, url=url))


class Tasks(commands.Cog, name="tasks"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        # start the task to run in the background
        self.monday_office_hour_reminder.start()

    @tasks.loop(time=datetime.time(hour=19, minute=30, tzinfo=ZoneInfo("America/New_York")))
    async def monday_office_hour_reminder(self):
        now = datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        if now.isoweekday() != 1:
            return

        channel = self.bot.get_channel(980353246361169950)
        office_hour_msg = """
@here **Happening now**

Staff Office hours - Weekly  

Casual office hours. Come chat in the Google Meet with the different chapters. Ask questions, get help, meet each other, etc. fully up to you!
"""
        await channel.send(
            content=office_hour_msg,
            view=LinkButton("Google meet", "https://meet.google.com/xnq-fdtk-ibh"),
        )
        print("sent")


async def setup(bot):
    await bot.add_cog(Tasks(bot))
