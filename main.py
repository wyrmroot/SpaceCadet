"""

Discord bot to report mining operations status
Based on tutorial at https://realpython.com/how-to-make-a-discord-bot-python/

#TODO: Keep track of downtime since error first occurred

"""

import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
from support import phoenix_connect


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
                                                        name='Initializing',
                                                        url=MONITOR_URL))
    while bot.is_ready():
        print('Fetching status')
        try:
            current_status = phoenix_connect.status_line()
            print(f'Got: {current_status}')
            if current_status['error']:
                await bot.change_presence(status=discord.Status.dnd,
                                          activity=discord.Activity(type=discord.ActivityType.playing,
                                                                    name=current_status['text'],
                                                                    url=MONITOR_URL))
                # TODO: Send alerts on failure
            else:
                await bot.change_presence(status=discord.Status.online,
                                          activity=discord.Activity(type=discord.ActivityType.playing,
                                                                    name=current_status['text'],
                                                                    url=MONITOR_URL))
        except Exception as e:
            print(f'Got error {e}')
            await bot.change_presence(status=discord.Status.dnd,
                                      activity=discord.Activity(type=discord.ActivityType.playing,
                                                                name="ERROR CONNECTING",
                                                                url=MONITOR_URL))
            # TODO: Send alerts on failure

        # Wait 1 minute (non-blocking)
        await asyncio.sleep(60)


@bot.command(name='status', help='Manually post a miner update')
async def status(ctx):
    miner_update = phoenix_connect.get_update()
    response = ""
    for key, val in miner_update.items():
        response += f"{key}: {val}\n"
    await ctx.send(response)


@bot.command(name='profit', help='Get daily profit in $USD based on mining rates')
async def profit(ctx):
    response = phoenix_connect.get_profit()
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


@bot.command(name='quit', help='Fully quit the bot script. Warning: Cannot be restarted from discord')
async def quit_prog(ctx):
    response = "Shutting down bot script on host :skull_crossbones:"
    print('Closing due to !quit command')
    await ctx.send(response)
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()


# Boot it up!
bot.run(TOKEN)
