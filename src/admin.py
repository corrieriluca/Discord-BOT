from discord.ext import commands
import discord

# The `!admin <A member nickname> command should create an Admin role with admin privileges
# on the server and give it to the member in parameter
@commands.command()
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if role is None:
        permissions = discord.Permissions(manage_channels=True, kick_members=True, ban_members=True)
        role = await ctx.guild.create_role(name="Admin", permissions=permissions)
    await member.add_roles(role)
    await ctx.send(f"{member.mention} You've been given the Admin role, with great power come great responsabilities!")

# The `!ban <A member nickname>` should ban the member in parameter from the server
@commands.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"{member.name} has been banned from the server.")

# The `!count` command should sort the members in the server based on their status
@commands.command()
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

# Function for the bot to setup command after this extension is loaded
async def setup(bot):
    bot.add_command(admin)
    bot.add_command(ban)
    bot.add_command(count)
