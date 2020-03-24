import discord
from discord.ext import commands, tasks

class MiscCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(description = "Gives the current ping of FERDA BOT - hosted on heroku")
    async def ping(self, ctx):
        """Displays ping of BOT """
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases = ["cl"], description = "amt - the amount of messages you would like to clear (Don't need to account for the actual command)")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amt):
        """Removes messages from channel"""
        await ctx.channel.purge(limit = int(amt) + 1)

def setup(client):
    client.add_cog(MiscCommands(client))
