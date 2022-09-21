from discord.ext import commands
import random

# `ping` command responds with `Pong!`
@commands.command()
async def ping(ctx):
    await ctx.send('Pong! :ping_pong:')

# `name` command responds with the username's sender
@commands.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

# `d6` command answers with a value between 1 and 6
@commands.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))

# Function for the bot to setup command after this extension is loaded
async def setup(bot):
    bot.add_command(ping)
    bot.add_command(name)
    bot.add_command(d6)
