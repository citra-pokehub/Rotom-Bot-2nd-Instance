from discord.ext import commands
import discord
import time
from math import floor
from replit import db
import asyncio


class AFK(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.group(invoke_without_command=True,
                    case_insensitive=True)
    async def afk(self, ctx, *, text = "AFK"):

        afks = db["afk"]

        if str(ctx.author.id) in afks:
            return await ctx.send(" <:uhh:880305186827014195> ")

        afks[str(ctx.author.id)] = {"afk": text, "time": round(time.time())}

        try:
            nickn = ctx.author.nick
            if not nickn:
                nickn = ctx.author.name
            
            if "[AFK]" in nickn:
                pass
            else:
                await ctx.author.edit(nick=f"[AFK] {nickn}")
        except:
            pass

        em = discord.Embed(title=f"{ctx.author} I set you AFK", description=text)

        await ctx.send(embed=em)

        db["afk"] = afks


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.guild.id != 770846450896470046 and message.guild.id != 676777139776913408:
            return

        afks = db["afk"]

        if str(message.author.id) in afks:

            time_remaining = round(time.time()) - afks[str(message.author.id)]['time']

            send = True

            hrs = floor(time_remaining/3600)
            mins = floor((time_remaining - hrs*3600)/60)
            secs = (time_remaining - hrs*3600 - mins*60)

            if hrs == 0 and mins == 0:
                if secs < 30:
                    send = False

            if send:
                del afks[str(message.author.id)]
                db["afk"] = afks

                try:
                    nickn = message.author.nick.replace("[AFK] ", "")

                    await message.author.edit(nick=f"{nickn}")
                except:
                    pass

                msg = await message.channel.send(f"{message.author.mention} I removed your AFK.")

                await asyncio.sleep(5)
                try:
                    await msg.delete()
                except:
                    pass

        if message.mentions:

            mentions = message.mentions

            for user in mentions:
                if str(user.id) in afks:

                    time_remaining = round(time.time()) - afks[str(user.id)]['time']

                    send = True

                    hrs = floor(time_remaining/3600)
                    mins = floor((time_remaining - hrs*3600)/60)
                    secs = (time_remaining - hrs*3600 - mins*60)

                    if hrs == 0 and mins == 0:
                        desc = f"{secs} seconds ago"
                    elif hrs == 0:
                        if mins == 1:
                            desc = f"{mins} minute ago"
                        else:
                            desc = f"{mins} minutes ago"
                    else:
                        if hrs == 1:
                            desc = f"{hrs} hour ago"
                        else:
                            desc = f"{hrs} hours ago"
                        
                    if send:

                        # mem = await self.client.fetch_user(user.id)

                        em = discord.Embed(title=f"{user.name} is AFK", description=afks[str(user.id)]['afk'], color=user.colour)
                        em.set_footer(text=desc)

                        await message.reply(embed=em, mention_author=False)

    @afk.command()
    @commands.has_role("moderator")
    async def reset(self, ctx, member:discord.Member):

        afks = db["afk"]
        afks[str(member.id)]["afk"] = "AFK"
        db["afk"] = afks

        await ctx.send(f"AFK status of {member} is reset.")

    
    @afk.command()
    @commands.has_role("moderator")
    async def clear(self, ctx, member:discord.Member):

        afks = db["afk"]
        del afks[str(member.id)]
        db["afk"] = afks

        try:
            nickn = member.nick.replace("[AFK] ", "")

            await member.edit(nick=f"{nickn}")
        except:
            pass

        await ctx.send(f"Removed AFK status of {member}.")


    @afk.command()
    @commands.has_role("moderator")
    async def list(self, ctx):

        afks = db["afk"]

        em = discord.Embed(title="AFK List")
        
        for mem in afks:

            user = await self.client.fetch_user(int(mem))

            time_remaining = round(time.time()) - afks[mem]['time']

            hrs = floor(time_remaining/3600)
            mins = floor((time_remaining - hrs*3600)/60)
            secs = (time_remaining - hrs*3600 - mins*60)

            if hrs == 0 and mins == 0:
                desc = f"{secs} seconds ago"
            elif hrs == 0:
                if mins == 1:
                    desc = f"{mins} minute ago"
                else:
                    desc = f"{mins} minutes ago"
            else:
                if hrs == 1:
                    desc = f"{hrs} hour ago"
                else:
                    desc = f"{hrs} hours ago"

            em.add_field(name=user.name, value=f"{afks[mem]['afk']} - {desc}", inline=False)

        await ctx.send(embed=em)
        


def setup(client): 
    client.add_cog(AFK(client))