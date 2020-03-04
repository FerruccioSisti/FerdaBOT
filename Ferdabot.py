import random, os, asyncio, discord, pymongo, json
import pandas as pd
import matplotlib.pyplot as plt
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime
from tabulate import tabulate
from pandas.plotting import table


DBPASS = str(os.environ.get("DBPASS"))
cluster = MongoClient(DBPASS)

db = cluster["Ferda"]
boys = db["TheBoys"]

client = commands.Bot(command_prefix = '>')

MAX_NAME_LENGTH = 20
MAX_REASON_LENGTH = 255

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
@commands.has_permissions(administrator=True)
async def add(ctx, user: discord.User, *name):
    """Add a newcomer to the boys"""
    
    fullname = ' '.join(name)

    if user == " " or fullname == " " or not user or not fullname:
        await ctx.send(f'wrong parameters idiot\n```{add.description}```')
        return

    if user not in client.users:
        return

    if len(fullname) > MAX_NAME_LENGTH:
        await ctx.send(f'{fullname} too long, use a nickname')
        return
    
    defaultjson = open("dbformat.json")
    data = json.load(defaultjson)

    data["name"] = fullname
    
    data["username"] = user.id

    data["log"].append("Added to the boys - " + str(datetime.today()))

    boys.insert(data)

    await ctx.send(f'{fullname} is now part of the brotherhood')

@client.command(description = "Displays the boys with their ferda points and bitchcards")
async def display(ctx):
    """Displays the boys with their ferda points and bitchcards"""

    all_boys = boys.find({})
    names = []
    points = []
    bcards = []

    for boy in all_boys:
        names.append(boy["name"])
        points.append(boy["points"])
        bcards.append(boy["bitchcard"])

    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    df = pd.DataFrame(
        {
            'Names' : names,
            'Ferda Points' : points,
            'Bitch Cards' : bcards
        }
    )

    table(ax, df, rowLabels=['']*df.shape[0], loc='center')

    plt.savefig("ferdatable.png")

    await ctx.send(file=discord.File('ferdatable.png'))


@client.command(description = "user - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're FERDA")
async def ferda(ctx, user: discord.User, *reason):
    """Recognize one of the boys for being FERDA"""
    fullreason = ' '.join(reason)

    if user == " " or fullreason == " " or not user or not fullreason:
        await ctx.send(f'wrong parameters idiot\n```{ferda.description}```')
        return

    if user not in client.users:
        return

    if boys.count_documents({"username": user.id}) == 0:
        await ctx.send(f'{user.name} not in db')
        return

    if len(fullreason) > MAX_REASON_LENGTH:
        await ctx.send(f'{fullreason} too long, please paraphrase')
        return

    


    ferda = boys.find_one_and_update(
        {"username":user.id},
        {
            "$inc":{"points":1},
            "$push":{"log":"+1 - " + fullreason + " - " + str(datetime.today())}
        }   
    )

    await ctx.send(f'{user.name} is so ferda')

@client.command(description = "user - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're not FERDA")
async def negferda(ctx, user: discord.User, reason):
    """Use this to be toxic and take away FERDA points"""
    fullreason = ' '.join(reason)

    if user == " " or fullreason == " " or not user or not fullreason:
        await ctx.send(f'wrong parameters idiot\n```{ferda.description}```')
        return

    if user not in client.users:
        return

    if boys.count_documents({"username": user.id}) == 0:
        await ctx.send(f'{user.name} not in db')
        return

    if len(fullreason) > MAX_REASON_LENGTH:
        await ctx.send(f'{fullreason} too long, please paraphrase')
        return

    ferda = boys.find_one_and_update(
        {"username":user.id},
        {
            "$inc":{"points":-1},
            "$push":{"log":"-1 - " + fullreason + " - " + str(datetime.today())}
        }   
    )
    # await ctx.author.send(":pinching_hand: :eggplant:")
    await ctx.send(f'{user.name} is so not ferda')

TOKEN = str(os.environ.get("TOKEN"))
client.run(TOKEN)
