import random
import os
import asyncio
import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '>')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #There currently isn't a way to set custom bot status', so for now we will use listening
    display = discord.Activity(name = "for '>' commands", type = 3)
    await client.change_presence(activity = display)


@client.command(description = "Gives the current ping of FERDA BOT - hosted on heroku")
async def ping(ctx):
    """Displays ping of BOT """
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases = ["cl"], description = "amt - the amount of messages you would like to clear (Don't need to account for the actual command)")
async def clear(ctx, amt):
    """Removes messages from channel"""
    await ctx.channel.purge(limit = int(amt) + 1)

@client.command(description = "name - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're FERDA")
async def ferda(ctx, name, reason):
    """Recognize one of the boys for being FERDA"""
    await ctx.send(f'{name} is so fucking FERDA')

TOKEN= str(os.environ.get("TOKEN"))
client.run(TOKEN)
