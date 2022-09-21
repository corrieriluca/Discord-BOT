from discord.ext import commands
import discord
import asyncio

import os
import random
import urllib.request
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 285491342895742977  # Discord ID of the bot owner, not always necessary

@bot.event
async def on_ready():  # When the bot is ready
    # Load all extensions
    await bot.load_extension('warmup') # warm-up commands
    await bot.load_extension('admin') # admin commands
    await bot.load_extension('fun') # fun and games commands

####### Warm-up commands -------------------------------------------------------

# Message `Salut tout le monde` should be responded with `Salut tout seul` and ping author
#
# Note: I did not find an easy way to put this in another file
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "Salut tout le monde":
        # Reply to the message, pinging original author
        await message.reply(f'Salut tout seul', mention_author=True)

    # Ensure other commands are still processed
    await bot.process_commands(message)

####### Fun commands -------------------------------------------------------

# The `!poll <question>` command should post a question and wait for reactions
# during 60 seconds, then delete the question and post results
#
# Note: did not manage to put it into another file too
@bot.command()
async def poll(ctx, question):
    main_message = await ctx.send("@here\n:bar_chart: Poll Time!\n" + question)
    message = await ctx.send(question + "\n\nReact to vote! (60 seconds) :alarm_clock:")
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    await asyncio.sleep(60)

    # This is needed to refresh the Message object and thus obtain correct number of reactions
    cache_msg = discord.utils.get(bot.cached_messages, id=message.id)

    positive = 0
    negative = 0
    for reaction in cache_msg.reactions:
        if reaction.emoji == "👍":
            positive = reaction.count - 1 # do not count the bot's reaction
        elif reaction.emoji == "👎":
            negative = reaction.count - 1

    await cache_msg.delete()

    await main_message.reply(f"Results: 👍 {positive} | 👎 {negative}")

token = os.environ.get("DISCORD_TOKEN") # Get the token from the environment variable
bot.run(token)  # Starts the bot
