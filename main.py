import discord as discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from replit import db
import asyncio

def get_prefix(client, message):
    """
    get bot prefix from database and set bot prefix for guild/server

    :param client: Discord.py client
    :param message: message sent in a server channel
    :return: bot prefix
    """
    if isinstance(message.channel, discord.channel.DMChannel):
        return "."
        
    guild = db["prefixes"]
    ret = guild.get(str(message.guild.id), ".")

    # if guild id not found in guilds list, set bot prefix to . and update database
    if str(message.guild.id) not in guild:
        guild[str(message.guild.id)] = "."

        db["prefixes"] = guild

    return ret

# initialize bot
prefix = get_prefix
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix,
                    intents=intents,
                    case_insensitive=True)


@client.event
async def on_ready():
    """ set up bot after login into discord servers successful """
    
    print(
        f"Bot is Ready.\nLogged in as {client.user.name}\n---------------------"
    )

    client.remove_command("help")

    # load cogs from directories
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)

    g = await client.fetch_guild(676777139776913408)

    invites = await g.invites()

    inv = {}

    for i in invites:
        inv[i.code] = i.uses

    db["invites"] = inv
    print("Invite data loaded!")



@client.event
async def on_message(message):
    """
    execute function whenever someone sends a message

    :param message: message string
    """
    if message.author == client.user:
        return

    pfx = get_prefix(client, message).lower()

    if message.channel.id == 761502109459677185 or message.channel.id == 856187354536214578:
        if message.author.id == 559426966151757824:
            await message.delete()

    if message.content.lower().startswith(pfx):
        message.content = message.content[:len(pfx)].lower() + message.content[len(pfx):]

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    """
    add guild id to db whenever bot joins a new server/guild

    :param guild: guild/server object
    """
    prefixes = db["prefixes"]
    prefixes[str(guild.id)] = "."
    db["prefixes"] = prefixes


@client.event
async def on_guild_leave(guild):
    """
    remove guild id from db whenever bot leaves a server/guild

    :param guild: guild/server object
    """
    prefixes = db["prefixes"]
    del prefixes[str(guild.id)]
    db["prefixes"] = prefixes


@client.event
async def on_command_error(ctx, error):
    """
    send error as message is bot command produces an error

    :param ctx: discord.py command context
    :param error: discord.py error object
    """
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, discord.errors.NotFound):
        pass
    else:
        try:
            msg = await ctx.send('{}'.format(str(error)))
            await asyncio.sleep(5)
            await msg.delete()
        except:
            pass


@client.command()
@commands.is_owner()
async def reload(ctx):
    """
    reload bot cogs/extensions

    :param ctx: discord.py command context
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")

    # await ctx.send("Extensions has been reloaded.")


keep_alive()
client.run(os.environ.get("TOKEN"))

# Rate Limit Fix: "kill 1"
