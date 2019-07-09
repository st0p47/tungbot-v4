from datetime import datetime
from discord.ext import commands
import discord
import config
import json
import urllib.request

prefix = config.prefix
bot = commands.Bot(command_prefix=prefix,
                   help_command=None,
                   activity=discord.Game("{}help".format(config.prefix)),
                   owner_id=config.owner_id
                   )

# Helper Methods


def getMCServerStatus(serverIP):
    api = "https://api.mcsrvstat.us/2/{}".format(config.server)
    with urllib.request.urlopen(api) as url:
        return json.loads(url.read().decode())


def standardEmbed(title, description):
    embed = discord.Embed(color=0x43efeb)
    embed.set_footer(text="tungbot-v4 | " +
                     datetime.now().strftime("%B %d, %Y, %H:%M:%S"))
    return embed


# Bot Methods
@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# @bot.event
# async def on_command_error(error, ctx):
#     if isinstance(error, commands.CommandOnCooldown):
#         await ctx.send("This command is on a %.2f second cooldown" % error.retry_after)

#     raise error


@bot.group()
async def server(ctx):
    """Group of commands to query the minecraft server"""
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid server command passed.')


@server.command()
@commands.cooldown(15, 60, commands.BucketType.guild)
async def status(ctx):
    """Get server status"""

    data = getMCServerStatus(config.server)

    title = "Server {}".format("Online" if data["online"] else "Offline")
    description = "Basic server status for minecraft server"

    embed = standardEmbed(title, description)
    embed.set_thumbnail(
        url="https://gamepedia.cursecdn.com/minecraft_gamepedia/4/44/Grass_Block_Revision_6.png"
    )
    embed.add_field(name="URL", value="{}:{}".format(
        config.server, data["port"]))

    if data["online"]:
        embed.add_field(name="MOTD", value=data["motd"]["raw"])
        embed.add_field(name="Version", value=data["version"])
        embed.add_field(name="Software", value=data["software"])
        embed.add_field(
            name="Capacity",
            value="{}/{}".format(
                data["players"]["online"],
                data["players"]["max"]
            )
        )

    await ctx.send(embed=embed)


@server.command()
@commands.cooldown(15, 60, commands.BucketType.guild)
async def players(ctx):
    """Get online players"""

    data = getMCServerStatus(config.server)

    title = "Players Online"
    description = "List of players online"
    embed = standardEmbed(title, description)
    embed.set_thumbnail(
        url="https://gamepedia.cursecdn.com/minecraft_gamepedia/4/44/Grass_Block_Revision_6.png"
    )

    if not data["online"]:
        embed.add_field(name="Server Offline")
        return
    else:
        embed.add_field(
            name="Capacity",
            value="{}/{}".format(
                data["players"]["online"],
                data["players"]["max"]
            )
        )

        await ctx.send(embed=embed)

        if data["players"].get("list") is not None:
            for player in list(data["players"]["list"]):
            title = "Player"
            description = ""
            playerEmbed = standardEmbed(title, description)

            playerEmbed.add_field(name="Player", value=player)
            playerEmbed.set_thumbnail(
                url="https://minotar.net/avatar/{}/300.png".format(player)
            )
            await ctx.send(embed=playerEmbed)


@bot.command()
async def shutdown(ctx):
    """For owners only: shutdown the bot"""
    yes = await bot.is_owner(ctx.message.author)
    if yes:
        await ctx.send("Successfully shutting down")
        await bot.close()
    else:
        await ctx.send("You cannot shut down this bot")


@bot.command()
async def screech(ctx):
    """Plays the infamous screech in the voice channel of sender"""

    print("Recieved command to screech")

    if ctx.message.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return

    channel = ctx.message.author.voice.channel

    voice = await channel.connect()

    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio("assets/screech.mp3"))
    await voice.play(source)

    await ctx.send('Now screeching!')

    await voice.disconnect()


@bot.command()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""

    print("leaving voice channel")
    await ctx.voice_client.disconnect()


@bot.command()
async def help(ctx, group=""):
    """Lists all bot functions"""

    embed = discord.Embed(
        title="Help",
        description="All commands explained here!",
        color=0x43efeb
    )

    embed.set_author(name="tungbot",
                     url="https://github.com/st0p47/tungbot-v4",
                     icon_url="https://st0p47.github.io/tungbot-v4_pfp.png")

    embed.set_footer(text="tungbot-v4 | " +
                     datetime.now().strftime("%B %d, %Y, %H:%M:%S"))

    # Super hacky because I got lazy
    if group == "server":
        for command in server.commands:
            embed.add_field(name=command.name,
                            value=command.short_doc, inline=False)
    else:
        for command in bot.commands:
            embed.add_field(name=command.name,
                            value=command.short_doc, inline=False)

    await ctx.send(embed=embed)

bot.run(config.token)
