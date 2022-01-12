from discord.ext import commands
import discord
from replit import db
import json

em_help = {
        "📛 Badge": "`{prefix}help badge`",
        "🎴 Pokedex": "`{prefix}help pokedex`",
        "🎮 Game": "`{prefix}help game`",
        "🎪 Fun": "`{prefix}help fun`",
        "🎶 Music": "`{prefix}help music`",
        "🎉 Misc": "`{prefix}help misc`"
}

def server_prefix(msg):

    if isinstance(msg.message.channel, discord.channel.DMChannel):
        return "."

    prefixes = db["prefixes"]
    s_prefix = prefixes[str(msg.guild.id)]

    return s_prefix


def help_em(command, prefix=""):

    main = "none"
    footer = ""
    drop = False

    with open("help_data.json", "r") as hd:
        data = json.load(hd)

    if command not in data:
        command = "main"

    if command == "main":
        des = f"If you need more information about a specific category, type `{prefix}help <category>` or select from below."
        title = "Categories"
        get = em_help
        main = "main"
        footer = f"Use {prefix}prefix [new_prefix] to change My Prefix."
        emoji = ""

    elif data[command]["cat"] == "cat":
        if data[command]["drop"] is True:
            des = f"If you need more information about a specific command, type `{prefix}help <command>` or Select the Command in Dropdown box."
            drop = True
        else:
            des = ""
            footer = "These commands don't have their Own Help command."
        main = "cat"
        title = f"{command.capitalize()} Commands"
        get = data[command]
        emoji = "<:reply:894413657365160016>"

    else:
        get = data[command]
        des = get["des"]
        if "footer" in get:
            footer = get["footer"]
        title = command.capitalize()
        emoji = ""

    em = discord.Embed(title=title, description=des, color=discord.Color.orange())

    em.set_footer(text=footer)

    for fields in get:
        if fields != "cat" and fields != "des" and fields != "footer" and fields != "drop":
            em.add_field(name=fields, value=f"{emoji}{get[fields].replace('{prefix}', prefix)}", inline=False)

    return em, main, drop


def get_cmd(cmd):
    with open("help_data.json", "r") as hd:
        data = json.load(hd)

    if data[cmd]:
        ret = data[cmd]
    else:
        ret = None

    return ret


class Dropdown(discord.ui.Select):
    def __init__(self, cmd):

        got = get_cmd(cmd)

        if got:
            options = []
            for i in got:
                if i != "cat" and i != "des" and i != "footer" and i != "drop":
                    options.append(discord.SelectOption(label=i, description=got[i]))

        else:
            options = [
                discord.SelectOption(label='Main', description='Return to Main Page.')
            ]

        super().__init__(placeholder='Commands', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        em = help_em(self.values[0].lower())
        await interaction.response.send_message(embed=em[0])


class DropdownView(discord.ui.View):

    def __init__(self, cmd):
        super().__init__(timeout=60)

        self.add_item(Dropdown(cmd))


class HelpButt(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='Badge', style=discord.ButtonStyle.green)
    async def badge(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("badge")
        view = DropdownView("badge")
        await interaction.response.send_message(embed=em[0], view=view)
        # await interaction.response.send_message(embed=em[0])


    @discord.ui.button(label='Pokedex', style=discord.ButtonStyle.green)
    async def pokedex(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("pokedex")
        view = DropdownView("pokedex")
        await interaction.response.send_message(embed=em[0], view=view)
        # await interaction.response.send_message(embed=em[0])


    @discord.ui.button(label='Game', style=discord.ButtonStyle.green)
    async def game(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("game")
        view = DropdownView("game")
        await interaction.response.send_message(embed=em[0], view=view)
        # await interaction.response.send_message(embed=em[0])


    @discord.ui.button(label='Fun', style=discord.ButtonStyle.green)
    async def fun(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("fun")
        # view = DropdownView("fun")
        # await interaction.response.send_message(embed=em[0], view=view)
        await interaction.response.send_message(embed=em[0])


    @discord.ui.button(label='Music', style=discord.ButtonStyle.green)
    async def music(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("music")
        # view = DropdownView("music")
        # await interaction.response.send_message(embed=em[0], view=view)
        await interaction.response.send_message(embed=em[0])

    @discord.ui.button(label='Misc', style=discord.ButtonStyle.green)
    async def misc(self, button: discord.ui.Button, interaction: discord.Interaction):
        em = help_em("misc")
        # view = DropdownView("misc")
        # await interaction.response.send_message(embed=em[0], view=view)
        await interaction.response.send_message(embed=em[0])


class HelpButtDis(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Badge', style=discord.ButtonStyle.green, disabled=True)
    async def badge(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


    @discord.ui.button(label='Pokedex', style=discord.ButtonStyle.green, disabled=True)
    async def pokedex(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


    @discord.ui.button(label='Game', style=discord.ButtonStyle.green, disabled=True)
    async def game(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


    @discord.ui.button(label='Fun', style=discord.ButtonStyle.green, disabled=True)
    async def fun(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


    @discord.ui.button(label='Music', style=discord.ButtonStyle.green, disabled=True)
    async def music(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


    @discord.ui.button(label='Misc', style=discord.ButtonStyle.green, disabled=True)
    async def misc(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=None):

        prefix = server_prefix(ctx)

        if command is not None:
            command = command.lower()

            with open("help_aliases.json", "r") as d:
                data = json.load(d)

            if command in data:
                command = data[command]
                
        else:
            command = "main"

        em, main, drop = help_em(command, prefix)
        em.set_thumbnail(url=self.client.user.display_avatar)

        if main == "main":
            view = HelpButt()
            view2 = HelpButtDis()
            msg = await ctx.send(embed=em, view=view)
            await view.wait()
            await msg.edit(embed=em, view=view2)
        elif main == "cat" and drop is True:
            view = DropdownView(command)
            msg = await ctx.send(embed=em, view=view)
            await view.wait()
            await msg.edit(embed=em, view=None)
        else:
            await ctx.send(embed=em)
            pass


def setup(client):
    client.add_cog(Help(client))