# event that bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} with ID: {bot.user.id}')

# event to check for unknown commands and inform user.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        user_sent_command = ctx.message.content
        await ctx.send(f'Command `{user_sent_command}` is not known. Please use `{settings.PREFIX}help` for a list of commands.')
    else:
        print(f'Error: {error}')

# event to send message to a channel when member joins the discord server
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        welcome_message = f'Welcome {member.mention} to this server!'
        await channel.send(welcome_message)
    else:
        print(f'No System Messages Channel was found.')

# event to send message to a channel when member leaves the discord server
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        goodbye_message = f'Goodbye {member.mention}!'
        await channel.send(goodbye_message)
    else:
        print(f'No System Messages Channel was found.')