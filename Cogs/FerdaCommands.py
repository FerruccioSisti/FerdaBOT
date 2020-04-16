import random, os, asyncio, discord, pymongo, json
import pandas as pd
import matplotlib.pyplot as plt
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime
from tabulate import tabulate
from pandas.plotting import table
import sys

sys.path.append("..") # Adds higher directory to python modules path.
import Config

DBPASS = str(os.environ.get("DBPASS"))
cluster = MongoClient(DBPASS)
db = cluster["Ferda"]
boys = db["TheBoys"]
MAX_NAME_LENGTH = 20
MAX_REASON_LENGTH = 255

class FerdaCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(description = "user - discord @ of who is being added to the boys\nname - name of who is being added to the boys")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.User, *name):
        """Add a newcomer to the boys"""

        fullname = ' '.join(name)

        #Checks if parameters are black or null
        if user == " " or fullname == " " or not user or not fullname:
            await ctx.send(f'wrong parameters idiot\n```{add.description}```')
            return

        #Checks if user is in server
        if user not in client.users:
            return

        #Makes sure name isn't too long
        if len(fullname) > MAX_NAME_LENGTH:
            await ctx.send(f'{fullname} too long, use a nickname')
            return

        defaultjson = open("../dbformat.json")
        data = json.load(defaultjson)

        data["name"] = fullname

        data["username"] = user.id

        data["log"].append("Added to the boys - " + str(datetime.today()))

        boys.insert(data)

        await ctx.send(f'{fullname} is now part of the brotherhood')

    @commands.command(description = "user - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're FERDA")
    async def ferda(self, ctx, user: discord.User, *reason):
        """Recognize one of the boys for being FERDA"""
        fullreason = ' '.join(reason)

        #Checks if parameters are black or null
        if user == " " or fullreason == " " or not user or not fullreason:
            await ctx.send(f'wrong parameters idiot\n```{ferda.description}```')
            return

        #Checks if user is in server
        if user not in self.client.users:
            return

        #Checks if person is in the db
        if boys.count_documents({"username": user.id}) == 0:
            await ctx.send(f'{user.name} not in db')
            return

        #Makes sure the author is not rewarding himself
        if ctx.author.id == user.id:
            await ctx.send("can't ferda yourself idiot")
            return

        #Makes sure reason is not too long
        if len(fullreason) > MAX_REASON_LENGTH:
            await ctx.send(f'{fullreason} too long, please paraphrase')
            return


        #Makes sure there is room for a vote
        if len(Config.vote_queue) > 2:
            await ctx.send('vote queue is full right, please complete a previous vote')
            return
        else:
            Config.vote_queue.append(ctx.message)


        print(str(user))
        print(ctx.message)
        print(Config.vote_queue)
        await ctx.message.add_reaction('✅')
        await ctx.message.add_reaction('❌')
        await ctx.send(f'Cast your vote above, is {user.name} ferda?')

    @commands.command(description = "user - discord @ of who you'd like to recognize for being FERDA\nreason - reason why they're not FERDA")
    async def negferda(self, ctx, user: discord.User, reason):
        """Use this to be toxic and take away FERDA points                             """
        fullreason = ' '.join(reason)

        if user == " " or fullreason == " " or not user or not fullreason:
            await ctx.send(f'wrong parameters idiot\n```{ferda.description}```')
            return

        if user not in self.client.users:
            return

        if boys.count_documents({"username": user.id}) == 0:
            await ctx.send(f'{user.name} not in db')
            return

        if ctx.author.id == user.id:
            await ctx.send("why would you wanted to negferda yourself? idiot")
            return

        if len(fullreason) > MAX_REASON_LENGTH:
            await ctx.send(f'{fullreason} too long, please paraphrase')
            return

        if len(Config.vote_queue) > 2:
            await ctx.send('vote queue is full right, please complete a previous vote')
            return
        else:
            Config.vote_queue.append(ctx.message)

        await ctx.message.add_reaction('✅')
        await ctx.message.add_reaction('❌')
        await ctx.send(f'Cast your vote above, is {user.name} not ferda?')

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

    @commands.command(description = "Displays the boys with their ferda points and bitchcards")
    async def display(self, ctx):
        """Displays the boys with their current stats"""

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

        #Hide the index in the dataframe
        df.style.hide_index()
        
        table(ax, df.sort_values(by=['Ferda Points'], ascending=False), rowLabels=['']*df.shape[0], loc='center')

        plt.savefig("ferdatable.png")

        await ctx.send(file=discord.File('ferdatable.png'))

def setup(client):
    client.add_cog(FerdaCommands(client))
