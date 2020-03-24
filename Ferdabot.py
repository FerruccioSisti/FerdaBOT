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
vote_queue = []

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #There currently isn't a way to set custom bot status', so for now we will use listening
    display = discord.Activity(name = "for '>' commands", type = 3)
    await client.change_presence(activity = display)

@client.event
async def on_reaction_add(reaction, user):
    #Checks if a reaction is added to a msg
    msg = reaction.message.content
    msgid = reaction.message
    channel = reaction.message.channel

    #If the msg is a poll, check for enough votes
    if msgid in vote_queue:
        if msg.startswith(">ferda"):
            if str(reaction) == '✅':
                if reaction.count >= 4:
                    name = decomp(msg)
                    vote_queue.remove(msgid)
                    await channel.send(f'Ferda vote passed {name} is so ferda')
            elif str(reaction) == '❌':
                if reaction.count >= 4:
                    vote_queue.remove(msgid)
                    await channel.send('Ferda vote failed :regional_indicator_l:')
            else:
                return
        elif msg.startswith(">negferda"):
            if str(reaction) == '✅':
                if reaction.count >= 4:
                    name = decomp(msg)
                    vote_queue.remove(msgid)
                    await channel.send(f'NegFerda vote passed {name} is so not ferda')
            elif str(reaction) == '❌':
                if reaction.count >= 4:
                    vote_queue.remove(msgid)
                    await channel.send('NegFerda vote failed :regional_indicator_w:')
            else:
                return
        else:
            return

def updateFerda(userid, points, fullreason):
    #Increments ones points
    ferda = boys.find_one_and_update(
        {"username":userid},
        {
            "$inc":{"points": points},
            "$push":{"log":"+1 - " + fullreason + " - " + str(datetime.today())}
        }
    )

def decomp(msg):
    #Decomping the msg string to get ferda or negferda, username and reason
    toks = [x.strip() for x in msg.split(' ')]
    inc =  1 if toks[0] == '>ferda' else -1
    user = toks[1][3:-1]
    fullreason = " ".join(toks[2:])
    updateFerda(int(user), inc, fullreason)

    return toks[1]

#Load all the extensions if this script is being executed
extensions = ['Cogs.FerdaCommands', 'Cogs.MiscCommands']
if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)

TOKEN= str(os.environ.get("TOKEN"))
client.run(TOKEN)
