from discord.ext import commands
import discord
import asyncio

import random
import urllib.request
import json

# The `!xkcd` command should post a random comic from https://xkcd.com/
@commands.command()
async def xkcd(ctx):
    # Get the latest comic number
    contents = urllib.request.urlopen("https://xkcd.com/info.0.json").read()
    data = json.loads(contents)
    latest = data["num"]

    # Get a random comic
    random_comic = random.randint(1, latest)
    contents = urllib.request.urlopen(f"https://xkcd.com/{random_comic}/info.0.json").read()
    data = json.loads(contents)

    comic_image_url = data["img"]
    description = data["alt"]

    # Create a beautiful response
    embed = discord.Embed(title=f"XKCD #{random_comic}", description=description)
    embed.set_image(url=comic_image_url)
    await ctx.send(embed=embed)

# Function for the bot to setup command after this extension is loaded
async def setup(bot):
    bot.add_command(xkcd)
