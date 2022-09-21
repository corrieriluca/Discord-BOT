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

# The `!count` command should count the number of members in the server based on their status
@bot.command()
async def count(ctx):
    online = 0
    offline = 0
    idle = 0
    dnd = 0
    for member in ctx.guild.members:
        if member.status == discord.Status.online:
            online += 1
        elif member.status == discord.Status.offline:
            offline += 1
        elif member.status == discord.Status.idle:
            idle += 1
        elif member.status == discord.Status.dnd:
            dnd += 1

    message = f"""
:bulb: **{online}** members are online,
:zzz: **{idle}** members are idle,
:no_entry: **{dnd}** members are in Do Not Disturb,
:ghost: **{offline}** members are offline.
    """
    await ctx.send(message)

token = os.environ.get("DISCORD_TOKEN") # Get the token from the environment variable
bot.run(token)  # Starts the bot
