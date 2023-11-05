# imports
import sys
import discord
from discord.ext import commands
import settings
import responses

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

# main function of bot with token check
def main():
    if settings.TOKEN is None:
        return ('no token was provided. Please provide token in .env file')
    try: bot.run(settings.TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error

# custom help menu from chatgpt -> I need to check this code and understand what it does and why its written as it is. Aim: be able to write this myself.
class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, or a category',
            'aliases': ['h']
        })

    async def send_bot_help(self, mapping):
        # Customize how bot-level help is displayed
        embed = discord.Embed(title=settings.BOT_NAME, description='Customized help for this bot.', color=discord.Color.blue())
        for cog, commands in mapping.items():
            command_list = []
            for command in commands:
                if not command.hidden:
                    command_list.append(f'`{command.name}` - {command.short_doc or "No description provided."}')
            if command_list:
                embed.add_field(name=cog.qualified_name if cog else "No Category", value='\n'.join(command_list), inline=False)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        # Customize how individual command help is displayed
        embed = discord.Embed(title=f'Command Help: {command.name}', description=command.help or "No description provided.", color=discord.Color.green())
        embed.add_field(name='Usage', value=f'`{self.get_command_signature(command)}`', inline=False)
        await self.context.send(embed=embed)

bot.help_command = CustomHelpCommand()

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

# event to to send message to a channel when member joins the discord server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(settings.WELCOME_CHANNEL))
    if channel:
        welcome_message = f'{member.name} just joined the Server!'
        await channel.send(welcome_message)
    else:
        print(f'Channel with ID {settings.WELCOME_CHANNEL} not found.')

# event to to send message to a channel when member leaves the discord server
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(settings.GOODBYE_CHANNEL))
    if channel:
        goodbye_message = f'{member.name} just left the server!'
        await channel.send(goodbye_message)
    else:
        print(f'Channel with ID {settings.GOODBYE_CHANNEL} not found.')

# example Command for Ping -> Pong
@bot.command(help='sends a pong as answer.',brief='sends a pong as answer.')
async def ping(ctx):
    await ctx.send('pong')

# command with fixed response from response.py file
@bot.command(help='sends a greeting message back.',brief='sends a greeting message back.')
async def hello(ctx):
    await ctx.send(responses.hello_response)

# command to clear channel for user provides {amount} of messages
@bot.command(help='clears messages in the channel.',brief='clears messages in the channel.')
async def clear(ctx, amount):
    await ctx.message.delete() # delete the command send by user before further deletions.
    if amount == 'all':
        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(message)
        await ctx.channel.delete_messages(messages)
        await ctx.send('All messages have been cleared.')
    else:
        amount = int(amount)
        amount = min(amount, 100) # limit the number of messages that can be cleared at once.
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages have been cleared')


# calling main function and printing out the errors from it.
if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        print(error)