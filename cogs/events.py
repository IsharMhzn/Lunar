from discord.ext import commands
from discord.utils import get
from utils import gsheets

import os
import csv

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moonhub_id = 938534503884947497
        self.admin_id = 573142243272294401
    
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
        gsheets.gs.write_new_member(f"{member.name}#{member.discriminator}")
        
    
def setup(bot):
    bot.add_cog(Events(bot))