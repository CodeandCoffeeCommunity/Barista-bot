import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks


class LinkButton(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()

        self.add_item(discord.ui.Button(label=label, url=url))


class Tasks(commands.Cog, name="tasks"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        # start the task to run in the background
        self.monday_office_hour_reminder.start()
        self.all_hands_reminder.start()

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

    @tasks.loop(time=datetime.time(hour=20, minute=25, tzinfo=ZoneInfo("America/New_York")))
    async def all_hands_reminder(self):
        now = datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        if now.day <= 7 and now.isoweekday() == 3:
            channel = self.bot.get_channel(980353246361169950)
            all_hands_msg = """
@here **Happening now**

Our **Monthly All Hands** meeting is **beginning in 5 minutes**.

Starting at **8:30pm EST / 7:30pm CST / 5:30pm PST**

After the meeting, we will be hosting an optional hangout session in the Discord voice channel from 9pm EST / 8pm CST / 6pm PST. This is a great opportunity to ask any questions you may have and connect with your fellow organizers and volunteers.

We look forward to seeing you there!

"""
            await channel.send(
                content=all_hands_msg,
                view=LinkButton("Google meet", "https://meet.google.com/fgd-kknr-ogh"),
            )
            print("done")
        else:
            return


async def setup(bot):
    await bot.add_cog(Tasks(bot))
