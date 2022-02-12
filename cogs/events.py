from discord.ext import commands
from discord.utils import get

import os
import csv

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moonhub_id = 938534503884947497
        self.admin_id = 789420559477899264
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild = get(self.bot.guilds, id=self.moonhub_id)
        admin = get(guild.members, id=self.admin_id)
        dm = await admin.create_dm()
        await dm.send(f"Ready: {self.bot.user} | Active Servers: {len(self.bot.guilds)}")

        print("Logged as:", self.bot.user)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.name} joined the server")
        user = member.name
        userid = member.id
        with open("./csv/users.csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)

            for u, uid, *c in csv_reader:
                if (int(uid) == userid):
                    print("User Info: Present")
                    return

        with open("./csv/users.csv", mode="a") as csv_file:
            csv_writer = csv.writer(csv_file)
            coins, cash, email = 5, 0, ""
            csv_writer.writerow([user, userid, coins, cash, email])   
    
def setup(bot):
    bot.add_cog(Events(bot))