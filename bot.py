from discord.ext.commands import Bot
from dotenv import load_dotenv

import os
import discord
import csv

load_dotenv()
TOKEN = os.getenv("TOKEN")

## bot
intents = discord.Intents().default()
intents.members = True
bot = Bot(command_prefix="/", intents=intents)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(TOKEN)