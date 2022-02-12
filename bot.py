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

# Create folder if does not exists
try:
    os.mkdir(os.path.join(os.curdir, "csv"))
except Exception as e:
    print("Error creating folder: ", e)


try:
    with open("./csv/users.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        if not "user" in header:
            raise Exception
except:
    with open("./csv/users.csv", mode="w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["user", "userid", "coins", "cash", "email"])

bot.run(TOKEN)