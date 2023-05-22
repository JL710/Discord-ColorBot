import discord
from discord.ext import commands
from datetime import datetime


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Bot {self.user} started!")

    async def on_application_command(self, ctx: discord.ApplicationContext, *args, **kwargs):
        print(datetime.now(), ctx.author.id, ctx.interaction.data)

bot = Bot(owner_id=398440299627544577)

bot.load_extension("Color")
bot.load_extension("ErrorHandler")


with open("token.txt", "r") as f:
    token = f.readline()

bot.run(token)