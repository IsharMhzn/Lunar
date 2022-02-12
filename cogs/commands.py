from discord.ext import commands
from discord.utils import get

import os
import csv
import re
import discord

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moonhub_id = 938534503884947497
        self.admin_id = 789420559477899264

    def check_if_dm(self, ctx):
        if not ctx.guild:
            guild = get(self.bot.guilds, id=self.moonhub_id)
            if user := get(guild.members, id=ctx.author.id):
                return user

    @commands.command()
    async def wallet(self, ctx):
        if user := self.check_if_dm(ctx):
            dm = await user.create_dm()
            userid = user.id

            with open("./csv/users.csv", mode="r") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)

                for u, uid, coin, cash, email in csv_reader:
                    if (int(uid) == userid):
                        await dm.send(f"**{user.name}** has **{coin} Crescent Coins** and **{cash} $** in their wallet.")
                        break
                else:
                    await dm.send("Please join the **Moonland** discord server to get your wallet.")
    
    @commands.command()
    async def link(self, ctx, email=None):
        if user := self.check_if_dm(ctx):
            dm = await user.create_dm()
            userid = user.id

            if not email:
                await dm.send("Please send your email as **/link example@moonland.com**")
                return

            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, email):
                csvlines = []
                with open("./csv/users.csv", mode="r") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csvlines.append(next(csv_reader))
                    for row in csv_reader:
                        uid = row[1]
                        if (int(uid) == userid):
                            row[-1] = email
                        csvlines.append(row)
                
                with open("./csv/users.csv", mode="w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(csvlines)    

                # guild = get(self.bot.guilds, id=self.moonhub_id)
                # member_role = get(guild.roles, name="Member")
                # await user.add_roles(member_role)
                await dm.send(":white_check_mark: Verifed.")          
            else:
                await dm.send("Your email/command is invalid. Recheck and try again.")

    @commands.command()
    async def send_message(self, ctx, textchannel=None):
        if not ctx.author.id == self.admin_id:
            return

        if not textchannel:
            await ctx.send("Try again: /send_message #channelexample")
            return

        textchannel = await commands.TextChannelConverter().convert(ctx, textchannel)
        if not isinstance(textchannel, discord.TextChannel):
            await ctx.send("Try again: /send_message #channelexample")
            return
        
        await ctx.send("Type the message and send it here...")
        msg = await self.bot.wait_for('message')
        await textchannel.send(msg.content)
    
    @commands.command()
    async def edit_message(self, ctx, messageid=None):
        if not ctx.author.id == self.admin_id:
            return
        
        if not messageid:
            await ctx.send("Try again: /edit_message messageid")
            return
        
        message = await ctx.fetch_message(messageid)
        if not message:
            await ctx.send("Invalid message id. Message not found.")
            return
        
        await ctx.send("**Edit the following message and send it again**\n" + message.content)
        msg = await self.bot.wait_for('message')
        await message.edit(content=msg.content)
        await ctx.reply("Edited the message :white_check_mark:")
        
        
def setup(bot):
    bot.add_cog(Commands(bot))