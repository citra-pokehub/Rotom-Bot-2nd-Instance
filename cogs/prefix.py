from discord.ext import commands
import discord
from replit import db
from datetime import datetime


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["change-prefix", "prefix"])
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new_prefix):
        prefixes = db["prefixes"]
        prefixes[(str(ctx.guild.id))] = new_prefix
        db["prefixes"] = prefixes
        # await ctx.send(f"Server Prefix has been changed to `{new_prefix}`")

    
    @commands.command()
    async def timestamp(self, ctx, *, dt=None):

        if dt == None:
            now = datetime.now(datetime.timezone.utc)
        else:
            dt += ", UTC"
            now = datetime.strptime(dt, '%d %m %Y, %H:%M:%S, %Z')

        timesta = int(datetime.timestamp(now))

        await ctx.send(timesta)
        

    @commands.command()
    async def countdown(self, ctx, *, dt=None):

        if dt == None:
            now = datetime.now()
        else:
            now = datetime.strptime(dt, '%d %m %Y, %H:%M:%S')

        timesta = int(datetime.timestamp(now))

        await ctx.send(f"<t:{timesta}:R>")

	
def setup(client):
    client.add_cog(Misc(client))
