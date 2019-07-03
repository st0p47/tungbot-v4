from discord.ext import commands
import discord
import config
from datetime import datetime

prefix = config.prefix
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.group()
async def server(ctx):
    pass


@server.command()
async def status(ctx):
    pass


@server.command()
async def players():
    pass

@bot.command()
async def screech(ctx):
    """Plays the infamous screech in the voice channel of sender"""

    print("Recieved command to screech")

    if ctx.message.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return

    channel = ctx.message.author.voice.channel

    await channel.connect()

    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio("assets/screech.mp3"))
    await ctx.voice_client.play(source, after=lambda e: print(
        'Player error: %s' % e) if e else None)

    await ctx.send('Now screeching!')

    await ctx.voice_client.disconnect()


@bot.command()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""

    print("leaving voice channel")
    await ctx.voice_client.disconnect()


botCommands = [screech, stop]


@bot.command()
async def help(ctx):
    """Lists all bot functions"""

    embed = discord.Embed(
        title="Help",
        description="All commands explained here!",
        color=0x43efeb)

    embed.set_author(name="tungbot",
                     url="https://github.com/st0p47/tungbot-v4",
                     icon_url="https://st0p47.github.io/tungbot-v4_pfp.png")

    embed.set_footer(text="tungbot-v4 | " +
                     datetime.now().strftime("%B %d, %Y, %H:%M:%S"))

    for command in bot.commands:
        embed.add_field(name=command.name, value=command.short_doc)

    await ctx.send(embed=embed)

bot.run(config.token)
