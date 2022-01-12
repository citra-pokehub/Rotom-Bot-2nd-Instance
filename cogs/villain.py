import discord
from discord.ext import commands, tasks
from replit import db
import asyncio
from math import floor
import time


async def vt(ctx, team):

    rm = ["team", "-", " "]
    for i in rm:
        text = team.lower().replace(i, "")

    # remove role
    async def rm_role():
        for team, role_id in team_role_ids.items():

            if role_id in [role.id for role in ctx.author.roles]:
                role_remove = discord.utils.get(ctx.guild.roles, id=role_id)

                await ctx.author.remove_roles(role_remove)

    # check if user wants to leave his current team without a joining new team
    team_role_ids = db["team_role_ids"]
    if text == 'none':

        for team, role_id in team_role_ids.items():

            if role_id in [role.id for role in ctx.author.roles]:
                role_remove = discord.utils.get(ctx.guild.roles, id=role_id)

                await ctx.author.remove_roles(role_remove)


                embed = discord.Embed(
                        description=f"**Your Current Team has been removed!**",
                        colour=discord.Colour.blue())

                # msg = await ctx.send(embed=embed)

                return embed

        embed = discord.Embed(
                description=f"**You are currently not in any team!**",
                colour=discord.Colour.blue())

        # msg = await ctx.send(embed=embed)

        return embed
                
    # check if member is currently in that team
    text = 'team-' + text
    if text in [role.name.lower() for role in ctx.author.roles]:
        embed = discord.Embed(
                description=f"**You are currently in that team!**",
                colour=discord.Colour.blue())

        # msg = await ctx.send(embed=embed)

        return embed
    
    # check if team joining is in roles list
    team_role_ids = db["team_role_ids"]
    if text not in list(team_role_ids.keys()):
        embed = discord.Embed(
                description=f"**This team does not exist.**",
                colour=discord.Colour.blue())

        # msg = await ctx.send(embed=embed)

        return embed

    # check if join team timer is reached
    grunt_timers = db["grunt_timers"]
    timer = grunt_timers.get(str(ctx.author.id))
    
    if str(ctx.author.id) in grunt_timers:
        time_limit = 172800   # in seconds
        if round(time.time()) - timer < time_limit:
            time_remaining = time_limit - (round(time.time()) - timer)

            hrs = floor(time_remaining/3600)
            mins = floor((time_remaining - hrs*3600)/60)
            secs = (time_remaining - hrs*3600 - mins*60)

            if hrs == 0 and mins == 0:
                description = f"**Please wait for another {secs} sec before changing your team.**"
            else:
                description = f"**Please wait for another {hrs} hr {mins} min before changing your team.**"

            embed = discord.Embed(
            description=description,
            colour=discord.Colour.blue())

            # msg = await ctx.channel.send(embed=embed)

            return embed
    
    # transfer from one team to another
    grunt_timers[str(ctx.author.id)] = round(time.time())
    
    await rm_role()

    # add new role
    role_add = discord.utils.get(ctx.guild.roles, name=text)
    await ctx.author.add_roles(role_add)
    # await ctx.message.add_reaction('👍')

    embed = discord.Embed(
            description=f"**You are a Member of {text} now.**",
            colour=discord.Colour.blue())
    db["grunt_timers"] = grunt_timers

    return embed


class VTButt(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx


    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        else:
            await interaction.response.send_message("This interaction is not for you.", ephemeral=True)
            return False


    @discord.ui.button(label='Rocket', style=discord.ButtonStyle.green, emoji="<:rocket:889828530039431209>")
    async def rocket(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = await vt(self.ctx, "rocket")
        await interaction.response.send_message(embed=em)
        pass

    @discord.ui.button(label='Magma', style=discord.ButtonStyle.green, emoji="<:magma:889828723963084840>")
    async def magma(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = await vt(self.ctx, "magma")
        await interaction.response.send_message(embed=em)
        pass


    @discord.ui.button(label='Galactic', style=discord.ButtonStyle.green, emoji="<:galactic:889828637698846760>")
    async def galactic(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = await vt(self.ctx, "galactic")
        await interaction.response.send_message(embed=em)
        pass


    @discord.ui.button(label='Plasma', style=discord.ButtonStyle.green, emoji="<:plasma:889828464385994763>")
    async def plasma(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = await vt(self.ctx, "plasma")
        await interaction.response.send_message(embed=em)
        pass

    @discord.ui.button(label='Skull', style=discord.ButtonStyle.green, emoji="<:skull:889828839541338163>")
    async def skull(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = await vt(self.ctx, "skull")
        await interaction.response.send_message(embed=em)
        pass


class VTButtDis(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label='Rocket', style=discord.ButtonStyle.green, emoji="<:rocket:889828530039431209>", disabled=True))

        self.add_item(discord.ui.Button(label='Magma', style=discord.ButtonStyle.green, emoji="<:magma:889828723963084840>", disabled=True))

        self.add_item(discord.ui.Button(label='Galactic', style=discord.ButtonStyle.green, emoji="<:galactic:889828637698846760>", disabled=True))

        self.add_item(discord.ui.Button(label='Plasma', style=discord.ButtonStyle.green, emoji="<:plasma:889828464385994763>", disabled=True))

        self.add_item(discord.ui.Button(label='Skull', style=discord.ButtonStyle.green, emoji="<:skull:889828839541338163>", disabled=True))


class Villain(commands.Cog):
    def __init__(self, client):
        self.client = client
    #     self.update_team_list.start()

    # def cog_unload(self):
    #     self.update_team_list.stop()


    async def up_lst(self):

        # TODO if possible can help to dynamically get guild id, im too lazy to look into it
        channel = self.client.get_channel(792627468774670388)
        roles = await self.client.get_guild(676777139776913408).fetch_roles()

        team_message_ids = db["team_message_ids"]
        team_emojis = list(db["team_emojis"].values())

        # get team roles from roles list
        team_roles = []
        for team, message_id in team_message_ids.items():
            for role in roles:
                if role.name == team:
                    team_roles.append(role)
                    break

        # Edit message by message ID
        for i, (team, message_id) in enumerate(team_message_ids.items()):
            team_name = team.split('-')[0].capitalize() + ' ' + team.split('-')[1].capitalize()
            msg = team_emojis[i] + ' **' + team_name + '** ' + team_emojis[i] + '\n'
            
            for i, mem in enumerate(team_roles[i].members):
                msg += str(i+1) + '. ' + mem.mention + '\n'
            
            if msg == team_name:
                msg += '1. No one'

            msg += '\n'
            message = await channel.fetch_message(message_id)
            await message.edit(content=msg)


    @commands.command(aliases=["jointeam", "jt"])
    async def join_team(self, ctx, *, text = ''):

        if ctx.channel.id != 791488051410239518 and ctx.channel.id != 847509607185383494:
            return

        # check if team parameter is given
        if text == '':
            embed = discord.Embed(
                    description=f"**Add a team name behind `.jointeam` or select below to join a villian team. The available villian teams are:**\nTeam Rocket <:rocket:889828530039431209>\nTeam Magma <:magma:889828723963084840>\nTeam Galactic <:galactic:889828637698846760>\nTeam Plasma <:plasma:889828464385994763>\nTeam Skull <:skull:889828839541338163>\n\n**To leave your current team, type `.jointeam none`**",
                    colour=discord.Colour.blue())

            view = VTButt(ctx)
            viewDis = VTButtDis()
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            await msg.edit(embed=embed, view=viewDis)

        else:
            ret = await vt(ctx, text)
            await ctx.send(embed=ret)

        await self.up_lst()
    

    @commands.command()
    @commands.has_role("moderator")
    async def upvt(self, ctx):
        if ctx.guild.id == 676777139776913408:
            await self.up_lst()
            await ctx.send("Updated!")

            
def setup(client):
    client.add_cog(Villain(client))
