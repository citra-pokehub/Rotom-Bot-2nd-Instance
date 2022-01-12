import discord as discord
from discord.ext import commands, tasks
import random
import os
import apraw
from urllib.parse import quote_plus

reddit = apraw.Reddit(client_id=os.environ.get("Cl_ID"),
                      client_secret=os.environ.get("Cl_S"),
                      username=os.environ.get("UN"),
                      password=os.environ.get("pass"),
                      user_agent=os.environ.get("UA")
)


meme_lst  = []

async def get_meme():

    global meme_lst

    subreddit = await reddit.subreddit("memes")

    meme_lst = []
    async for subm in subreddit.hot(limit=500):
        meme_lst.append(subm)


class InvButt(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label='Click Here', style=discord.ButtonStyle.green, url="https://discord.com/api/oauth2/authorize?client_id=783598148039868426&permissions=2684674112&scope=bot"))

class BumpButt(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label='Click Here', style=discord.ButtonStyle.green, url="https://discordservers.com/server/676777139776913408/bump"))

class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'

        self.add_item(discord.ui.Button(label='Click Here', url=url))


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.meme_loop.start()

    def cog_unload(self):
        self.meme_loop.stop()

    @commands.command()
    async def meme(self, ctx):

        global meme_lst

        rand = random.choice(meme_lst)

        em = discord.Embed(title=rand.title)
        em.set_image(url=rand.url)

        await ctx.send(embed=em)


    @tasks.loop(hours=1)
    async def meme_loop(self):
        await get_meme()

    @commands.command(aliases=['ub'])
    async def userbanner(self, ctx, *, member:discord.Member = None):

        if member is None:
            member = ctx.author.id
        else:
            member = member.id

        mem = await self.client.fetch_user(member)

        em = discord.Embed(title=f"{mem}'s Banner")
        
        try:
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        except:
            return

        try:
            em.set_image(url=mem.banner)

            await ctx.send(embed=em)
        except:
            await ctx.send(f"{mem} have no Banner.")

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):

        if member is None:
            member = ctx.author

        em = discord.Embed(title=f"{member}'s Avatar")
        em.set_image(url=member.display_avatar)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @commands.command()
    async def invite(self, ctx):

        em = discord.Embed(title="__Invite Me in your Server__",
            colour=discord.Colour.orange())

        await ctx.send(embed=em, view=InvButt())


    @commands.command(aliases=["c", "calculator"])
    async def calculate(self, ctx, expression):
        await ctx.send(eval(expression))

    # @commands.command()
    # async def googletry(self, ctx, *, query: str):
    #     await ctx.send(f'Google Result for: `{query}`', view=Google(query))


def setup(client):
    client.add_cog(Setup(client))