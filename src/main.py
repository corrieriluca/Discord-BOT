from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
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
    import random
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

token = os.environ.get("DISCORD_TOKEN") # Get the token from the environment variable
bot.run(token)  # Starts the bot
