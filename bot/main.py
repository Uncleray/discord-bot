import sys
from colorama import Back, Fore, Style
import platform
import time
import datetime
import discord
from discord.ext import commands
from discord import app_commands
import settings

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# main function of bot with token check
def main():
    if settings.TOKEN is None:
        return ('no token was provided. Please provide token in .env file')
    try: discord_bot.run(settings.TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error

# defining Class of Bot
class CherryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=settings.PREFIX, intents=intents)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime('%H:%M:%S UTC', time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f'{prfx} Logged in as: {Fore.BLUE}{self.user.name}')
        print(f'{prfx} Bot ID: {Fore.YELLOW}{self.user.id}')
        print(f'{prfx} Discord Version: {Fore.YELLOW}{discord.__version__}')
        print(f'{prfx} Python Version: {Fore.YELLOW}{platform.python_version()}')
        synced_commands = await self.tree.sync()
        print(f'{prfx} Slash Commands Synced: {Fore.YELLOW}{len(synced_commands)}')

discord_bot = CherryBot()

"""
Trying to get Slash Commands working.
"""
# Command that will send Ping back to user
@discord_bot.tree.command(name='ping',description='Will send a Pong back!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(content='Pong!')

# Command that will show Information of Author or a target user
@discord_bot.tree.command(name='userinfo',description='Display information on User')
async def userinfo(interaction: discord.Interaction, member:discord.Member=None):
    if member == None:
        member = interaction.user
    roles = [role for role in member.roles]
    embed = discord.Embed(title='User Info',description=f'Here is the information you requested of User {member.mention}.',color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name='Nickname',value=member.display_name)
    embed.add_field(name='Username',value=f'{member.name}')
    embed.add_field(name='ID',value=member.id)
    embed.add_field(name='Top Role',value=member.top_role.mention)
    embed.add_field(name=f'Roles ({len(roles)})', value=" " .join([role.mention for role in roles]))
    embed.add_field(name='Status',value=member.status)
    embed.add_field(name='Activity',value=member.activity)
    embed.add_field(name='Created at',value=member.created_at.strftime('%a. %B %d, %Y, %I:%M %p'))
    embed.add_field(name='Joined at',value=member.joined_at.strftime('%a. %B %d, %Y, %I:%M %p'))
    await interaction.response.send_message(embed=embed,ephemeral=False)

# Command that will show Information about the Server
@discord_bot.tree.command(name='serverinfo',description='Display information on the Server')
@app_commands.checks.has_any_role('Moderator','SuperUser','ServerOWner')
async def serverinfo(interaction: discord.Interaction):
    embed = discord.Embed(title='Server Info',description='Here is the information you requested about the server.',color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.add_field(name='Server Name',value=interaction.guild.name)
    embed.add_field(name='Owner',value=interaction.guild.owner.mention)
    embed.add_field(name='Channels',value=f'Text {len(interaction.guild.text_channels)} | Voice {len(interaction.guild.voice_channels)}')
    await interaction.response.send_message(embed=embed,ephemeral=False)

# command to clear channel for user provides {amount} of messages
"""
Needs to be fixed. Throws Error 404 - Unknown Interaction
"""
@discord_bot.tree.command(name='clear',description='clears amount of messages in channel')
async def clear(interaction: discord.Interaction, amount:int):
        amount = min(amount, 100) # limit the number of messages that can be cleared at once.
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'{amount} messages have been cleared')

"""
Trying to create a permission-issue command to let the user know he does not have enough permission to run the command he wanted to.
"""
# calling main function and printing out the errors from it.
if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        print(error)