import discord
from discord.ext import commands


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Bot {self.user} started!")

bot = Bot(owner_id=398440299627544577)

bot.load_extension("Color")
bot.load_extension("ErrorHandler")


with open("token.txt", "r") as f:
    token = f.readline()

bot.run(token)