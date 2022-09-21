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

bot.author_id = 285491342895742977  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

####### Warm-up commands -------------------------------------------------------

# `ping` command responds with `Pong!`
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! :ping_pong:')

# `name` command responds with the username's sender
@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

# `d6` command answers with a value between 1 and 6
@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))

# Message `Salut tout le monde` should be responded with `Salut tout seul` and ping author
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "Salut tout le monde":
        # Reply to the message, pinging original author
        await message.reply(f'Salut tout seul', mention_author=True)

    # Ensure other commands are still processed
    await bot.process_commands(message)

####### Administration commands ------------------------------------------------

# The `!admin <A member nickname> command should create an Admin role with admin privileges
# on the server and give it to the member in parameter
@bot.command()
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if role is None:
        permissions = discord.Permissions(manage_channels=True, kick_members=True, ban_members=True)
        role = await ctx.guild.create_role(name="Admin", permissions=permissions)
    await member.add_roles(role)
    await ctx.send(f"{member.mention} You've been given the Admin role, with great power come great responsabilities!")

# The `!ban <A member nickname>` should ban the member in parameter from the server
@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"{member.name} has been banned from the server.")

# The `!count` command should sort the members in the server based on their status
@bot.command()
async def count(ctx):
    online = [member.name for member in ctx.guild.members if member.status == discord.Status.online]
    offline = [member.name for member in ctx.guild.members if member.status == discord.Status.offline]
    idle = [member.name for member in ctx.guild.members if member.status == discord.Status.idle]
    dnd = [member.name for member in ctx.guild.members if member.status == discord.Status.dnd]

    message = f"""
:bulb: **{len(online)} members are online:** {', '.join(online)}
:zzz: **{len(idle)} members are idle:** {', '.join(idle)}
:no_entry: **{len(dnd)} members are in Do Not Disturb:** {', '.join(dnd)}
:ghost: **{len(offline)} members are offline:** {', '.join(offline)}
    """

    await ctx.send(message)

####### Fun and games commands -------------------------------------------------

# The `!xkcd` command should post a random comic from https://xkcd.com/
@bot.command()
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

# The `!poll <question>` command should post a question and wait for reactions
# during 60 seconds, then delete the question and post results
@bot.command()
async def poll(ctx, question):
    main_message = await ctx.send("@here\n:bar_chart: Poll Time!\n" + question)
    message = await ctx.send(question + "\n\nReact to vote! (60 seconds) :alarm_clock:")
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    await asyncio.sleep(60)

    # This is needed to refresh the Message object and thus obtain correct number of reactions
    cache_msg = discord.utils.get(bot.cached_messages, id=message.id)

    for reaction in cache_msg.reactions:
        if reaction.emoji == "👍":
            positive = reaction.count - 1
        elif reaction.emoji == "👎":
            negative = reaction.count - 1

    await cache_msg.delete()

    await main_message.reply(f"Results: 👍 {positive} | 👎 {negative}")

token = os.environ.get("DISCORD_TOKEN") # Get the token from the environment variable
bot.run(token)  # Starts the bot
