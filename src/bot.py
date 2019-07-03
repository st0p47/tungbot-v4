from discord.ext import commands
import discord
import config

prefix = config.prefix
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    print("The message's content was", message.content)

    await bot.process_commands(message)


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

bot.run(config.token)
