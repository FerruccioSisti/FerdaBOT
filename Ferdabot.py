import random
import os
import asyncio
import discord
import pymongo
import json
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime
from tabulate import tabulate

cluster = MongoClient("mongodb+srv://arshDB:arshDBpass@cluster0-hbjvs.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Ferda"]
boys = db["TheBoys"]

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

@client.command(description = "user - discord @ of who is being added to the boys\nname - name of who is being added to the boys")
async def add(ctx, user, *name):
    """Add a newcomer to the boys"""
    
    fullname = ' '.join(name)
    defaultjson = open("dbformat.json")
    data = json.load(defaultjson)

    data["name"] = fullname
    data["username"] = user
    data["log"].append("Added to the boys - " + str(datetime.today()))

    boys.insert(data)

    await ctx.send(f'{fullname} is now part of the brotherhood')

@client.command(description = "Displays the boys with their ferda points and bitchcards")
async def display(ctx):
    """Displays the boys with their ferda points and bitchcards"""
    
    all_boys = boys.find({})
    out_string = []

    for boy in all_boys:
        out_string.append([boy["name"], str(boy["points"]), str(boy["bitchcard"])])

    table = tabulate(out_string, headers=["Name", "Ferda Points", "Bitch Cards"])

    await ctx.send(f'```{table}```')

@client.command(description = "name - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're FERDA")
async def ferda(ctx, name, reason):
    """Recognize one of the boys for being FERDA"""
    await ctx.send(f'{name} is so fucking FERDA')

@client.command(description = "name - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're not FERDA")
async def negferda(ctx, name, reason):
    """Use this to be toxic and take away FERDA points"""
    await ctx.author.send(":pinching_hand: :eggplant:")

@client.command(description = "name - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're not FERDA")
async def test(ctx, name, reason):
    """Use this to be toxic and take away FERDA points"""
    await ctx.send(":pinching_hand: :eggplant:")

TOKEN= str(os.environ.get("TOKEN"))
client.run("NjgyMDg4MjI5NTQwODU1ODk5.XlwX_w.tzovVbHdKXT573AhiSaoxeGGKAM")
