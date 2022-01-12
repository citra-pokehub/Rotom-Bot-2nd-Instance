import json
import string
import difflib
import discord
from discord.ext import commands
import time

genLst = {1: "rb", 2: "gs", 3: "rs", 4: "dp", 5: "bw", 6: "xy", 7: "sm", 8: "ss"}
genLstr = {"rb": "1", "gs": "2", "rs": "3", "dp": "4", "bw": "5", "xy": "6", "sm": "7", "ss": "8"}


def get_mon(find, gen):
    with open("data/pokedex.json", "r") as load:
        data = json.load(load)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    with open(f"sets/{genLst[gen]}.json", "r") as f:
        sets = json.load(f)

    def rm(s):
        rmd = s.replace(" ", "")
        rmd = rmd.replace("-", "")
        return rmd.lower()

    find1 = find.translate(
        str.maketrans('', '', string.punctuation))

    if find1 in data["Pokedex"]:
        if "forme" in data["Pokedex"][find1]:
            if data["Pokedex"][find1]["forme"] == "Mega" or data["Pokedex"][find1]["forme"] == "Mega-X" or \
                    data["Pokedex"][find1]["forme"] == "Mega-Y":
                ret = rm(data["Pokedex"][find1]["baseSpecies"])
                return ret

        if find1 not in sets:
            try:
                ret = rm(data["Pokedex"][find1]["baseSpecies"])
            except KeyError:
                return None
            return ret

        return find1.lower()

    if find1 in lit["Pokedex"]:
        mod = lit["Pokedex"][find1]
        if "forme" in data["Pokedex"][mod]:
            if data["Pokedex"][mod]["forme"] == "Mega" or data["Pokedex"][mod]["forme"] == "Mega-X" or \
                    data["Pokedex"][mod]["forme"] == "Mega-Y":
                ret = rm(data["Pokedex"][mod]["baseSpecies"])
                return ret

        if mod not in sets:
            try:
                ret = rm(data["Pokedex"][mod]["baseSpecies"])
            except KeyError:
                return None
            return ret

        return mod.lower()

    match = difflib.get_close_matches(find1, data["Pokedex"], 1)

    if match:
        fnd = match[0]
        if "forme" in data["Pokedex"][fnd]:
            if data["Pokedex"][fnd]["forme"] == "Mega" or data["Pokedex"][fnd]["forme"] == "Mega-X" or \
                    data["Pokedex"][fnd]["forme"] == "Mega-Y":
                ret = rm(data["Pokedex"][fnd]["baseSpecies"])
                return ret

        if fnd not in sets:
            try:
                ret = rm(data["Pokedex"][fnd]["baseSpecies"])
            except KeyError:
                return None
            return ret

        return fnd.lower()

    return "None"


def get_mats(mon, gen):
    with open(f"sets/{genLst[gen]}.json", "r") as f:
        data = json.load(f)

    format = []

    for mats in data[mon]:
        format.append(mats["format"])

    return format


def get_spid(mon):
    with open("data/pokedex.json", "r") as load:
        data = json.load(load)

    spID = data["Pokedex"][mon]["name"]

    spID = spID.replace("’", "").lower()
    spID = spID.replace(" ", "")

    if spID == "darmanitan-galar-zen":
        spID = "darmanitan-galarzen"

    if "o-o" in spID:
        if spID != "kommo-o-totem":
            spID = spID.replace("o-o", "oo")

    if spID.endswith("-star"):
        spId = spID.replace("-star", "star")

    if "striped" in spID:
        spId = spID.replace("-striped", "striped")

    if "pom-pom" in spID:
        spId = spID.replace("-pom", "pom")

    if "dusk-mane" in spID:
        spId = spID.replace("-mane", "mane")

    if "dawn-wing" in spID:
        spId = spID.replace("-wing", "wing")

    if "low-key" in spID:
        if "gmax" in spID:
            spId = spID.replace("low-key", "")
        else:
            spId = spID.replace("low-key", "lowkey")

    if "urshifu" in spID:
        if "gmax" in spID:
            spId = spID.replace("-gmax", "")

        if "rapid" in spID:
            spId = spID.replace("-strike", "strike")

    if "mega-x" in spID:
        spID = spID.replace("mega-x", "megax")

    if "mega-y" in spID:
        spID = spID.replace("mega-y", "megay")

    return spID


def get_sets(mon, gen, ind, pg):
    with open(f"sets/{genLst[gen]}.json", "r") as f:
        data = json.load(f)

    if ind == "None":
        return None

    format = get_mats(mon, gen)
    inx = format.index(ind)

    tot_sets = len(data[mon][inx]["movesets"])

    if pg > tot_sets:
        return None

    get = data[mon][inx]["movesets"][pg - 1]

    item = ""
    ability = ""
    evs = ""
    ivs = ""
    nature = ""
    move = ""

    if get['items']:
        item = get['items'][0]

    if get['abilities']:
        ability = f"Ability: {get['abilities'][0]}"

    if get['natures']:
        nature = f"{get['natures'][0]} Nature"

    if get['moveslots']:
        for i in get['moveslots']:
            move += f"- {i[0]['move']}"
            if i[0]['type']:
                move += f" {i[0]['type'].capitalize()}"
            move += "\n"

    stat_lst = {"hp": "HP", "atk": "Atk", "def": "Def", "spa": "SpA", "spd": "SpD", "spe": "Spe"}
    if get['ivconfigs']:
        for i in get["evconfigs"][0]:
            if get["evconfigs"][0][i] != 0:
                evs += f" {get['evconfigs'][0][i]} {stat_lst[i]} /"

    if get['ivconfigs']:
        for i in get["ivconfigs"][0]:
            if get["ivconfigs"][0][i] != 31:
                ivs += f" {get['ivconfigs'][0][i]} {stat_lst[i]} /"

    form = f"{get['pokemon']}"
    if item != "":
        form += f" @ {item}"
    if ability != "":
        form += f"\n{ability}"
    if evs != "":
        form += f"\nEVs:{evs[:-1]}"
    if ivs != "":
        form += f"\nIVs:{ivs[:-1]}"
    if nature != "":
        form += "\n" + nature
    if move != "":
        form += "\n" + move

    spID = get_spid(mon)
    sprite = f"https://play.pokemonshowdown.com/sprites/ani/{spID}.gif"

    em = discord.Embed(title=f"Gen {gen} {ind} Sets for {mon.capitalize()}", description=f"**{get['name']}**\n{form}", color=discord.Color.orange())
    em.set_thumbnail(url=sprite)
    em.set_footer(text=f"Set {pg} out of {tot_sets}.")

    return em, tot_sets


class NavButt(discord.ui.View):
    def __init__(self, page, cur, mon, gen, format):
        self.page = page
        self.cur = cur
        self.mon = mon
        self.gen = gen
        self.format = format
        super().__init__(timeout=60)


    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.primary)
    async def left(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.cur-1 >= 1:
            # button.disabled = False
            em = get_sets(self.mon, self.gen, self.format, self.cur-1)
            view = NavButt(em[1], self.cur-1, self.mon, self.gen, self.format)
            await interaction.response.edit_message(embed=em[0], view=view)
        else:
        #     button.disabled = True
        #     await interaction.response.edit_message(view=self)
            await interaction.response.send_message("No previos page available.", ephemeral=True)


    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.primary)
    async def right(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.cur+1 <= self.page:
            em = get_sets(self.mon, self.gen, self.format, self.cur+1)
            view = NavButt(em[1], self.cur+1, self.mon, self.gen, self.format)
            await interaction.response.edit_message(embed=em[0], view=view)
        else:
            await interaction.response.send_message("No next page available.", ephemeral=True)


class Dropdown(discord.ui.Select):
    def __init__(self, mon, gen):
        self.mon = mon
        self.gen = gen

        got = get_mats(mon, gen)

        if got:
            options = []
            for i in got:
                options.append(discord.SelectOption(label=i, description=f"Sets of {i} Format."))

        else:
            options = [
                discord.SelectOption(label='None', description='No Format for this Pokemon.')
            ]

        super().__init__(placeholder='Formats', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        em = get_sets(self.mon, self.gen, self.values[0], 1)
        if em:
            view = NavButt(em[1], 1, self.mon, self.gen, self.values[0])
            await interaction.response.send_message(embed=em[0], view=view)


class DropdownDis(discord.ui.Select):
    def __init__(self):
        
        options = [
            discord.SelectOption(label='None', description='No Format for this Pokemon.')
        ]

        super().__init__(placeholder='Formats', min_values=1, max_values=1, options=options, disabled=True)


class DropdownView(discord.ui.View):

    def __init__(self, mon, gen):
        super().__init__()

        self.add_item(Dropdown(mon, gen))


class DropdownViewDis(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(DropdownDis())


class PkDex3(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["moveset", "smogon"])
    async def sets(self, ctx, mon, *, gen="8"):
        
        # if ctx.author.id != 549415697726439434:
        #     return

        gen = gen.replace(" ", "")
        gen = gen.lower().replace("gen", "")

        if gen in genLstr:
            gen = genLstr[gen]

        if not gen.isnumeric():
            return await ctx.send("That's not a valid generation, use numbers from 1 to 8 or gen code.")

        avai = [1, 2, 3, 4, 5, 6, 7, 8]

        if int(gen) not in avai:
            return await ctx.send("That's not a valid generation, use numbers from 1 to 8 or gen code.")

        pm = get_mon(mon, int(gen))

        if not pm:
            return await ctx.send("Pokémon not in this generation.")
        elif pm == "None":
            return await ctx.send("Pokémon not found.")

        # async with ctx.typing():
        view = DropdownView(pm, int(gen))
        msg = await ctx.send("Select Format from below.", view=view)
            
        await view.wait()
        viewDis = DropdownViewDis()
        await msg.edit(view=viewDis)


def setup(client):
    client.add_cog(PkDex3(client))
