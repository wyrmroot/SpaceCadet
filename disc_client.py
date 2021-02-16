"""

Discord bot to report mining operations status
Based on tutorial at https://realpython.com/how-to-make-a-discord-bot-python/

"""

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


# Load secrets from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONITOR_URL = os.getenv('SERVER_URL')
LOG_CHANNEL = os.getenv('DISCORD_CHANNEL')

# Establish bot client object and its keyword
bot = commands.Bot(command_prefix='!')


# Event that runs once login is successful
@bot.event
async def on_ready():
    print('Triggered the on_ready function')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} successfully connected to the following server:\n'
          f'{guild.name} (id: {guild.id})\n')
    # Start as idle, update to online once we connect to server
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(type=discord.ActivityType.playing,
                                                        name='Idle',
                                                        url=MONITOR_URL))


@bot.command(name='status', help='Manually post a miner update')
async def status(ctx):
    response = "Bot is live :tada: \n" \
               "Server is not yet connected :skull_crossbones: "
    await ctx.send(response)


@bot.command(name='pause', help='Stop automatically checking miner status')
async def pause_updates(ctx):
    # TODO: Actually change behavior
    response = ":red_square: Automatic updates disabled (turn back on with `!resume`)"
    await ctx.send(response)
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(type=discord.ActivityType.playing,
                                                        name='Paused',
                                                        url=MONITOR_URL))


@bot.command(name='resume', help='Stop automatically checking miner status')
async def resume_updates(ctx):
    # TODO: Actually change behavior
    response = ":green_circle: Automatic updates resumed"
    await ctx.send(response)
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.playing,
                                                        name='290 MH/s, 1016W',
                                                        url=MONITOR_URL))


@bot.command(name='freq', help='Change update frequency to every # minutes')
async def freq(ctx, a: int):
    if a < 1:
        response = "ERR: Can't update less than 1 min apart."
    elif a > 1440:
        response = "WARN: Setting to 1440 min (1 day)."
    else:
        response = f"Now updating every {a} minutes."
    await ctx.send(response)


@bot.command(name='gpu', help='List GPU temps and speeds')
async def gpu(ctx):
    response = f"Checking status of each GPU"
    await ctx.send(response)


@bot.command(name='test', help='Test routine to change presence')
async def test(ctx, p: int):
    # TODO: Call the function that talks to the mining server
    if p == 0:
        response = "Switching to online (default)"
        await bot.change_presence(status=discord.Status.online)
    elif p == 1:
        response = "Switching to connected"
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name='290 MH/s, 1016W',
                                                            url=MONITOR_URL))
    elif p == 2:
        response = "Switching to idle (paused)"
        await bot.change_presence(status=discord.Status.idle,
                                  activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name='Paused',
                                                            url=MONITOR_URL))
    elif p == 3:
        response = "Switching to DND (error)"
        await bot.change_presence(status=discord.Status.dnd,
                                  activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name='ERROR',
                                                            url=MONITOR_URL))
    elif p == 4:
        response = "Switching to custom status"
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.CustomActivity(name='Super awesome custom'))
    else:
        response = "ERR: Bad argument found"

    # Wrap up and send
    if response:
        await ctx.send(response)


@bot.command(name='quit', help='Fully quit the bot script. Warning: Cannot be restarted from discord')
async def quit_prog(ctx):
    response = "Shutting down bot script on host :skull_crossbones:"
    print('Closing due to !quit command')
    await ctx.send(response)
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()


# Boot it up!
bot.run(TOKEN)
