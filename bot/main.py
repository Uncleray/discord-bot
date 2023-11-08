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
@app_commands.checks.has_any_role('Moderator','SuperUser','Server Owner')
async def serverinfo(interaction: discord.Interaction):
    embed = discord.Embed(title='Server Info',description='Here is the information you requested about the server.',color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.add_field(name='Server Name',value=interaction.guild.name)
    embed.add_field(name='Owner',value=interaction.guild.owner.mention)
    embed.add_field(name='Channels',value=f'Text {len(interaction.guild.text_channels)} | Voice {len(interaction.guild.voice_channels)}')
    await interaction.response.send_message(embed=embed,ephemeral=False)

# command to purge messages in channel. Limited to 100 messages each purge.
@discord_bot.tree.command(name= "purge", description="Purge messages in a channel")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    amount = min(amount, 100) # limit the number of messages that can be cleared at once.
    await interaction.channel.purge(limit=amount)
    embed = discord.Embed(description=f"Purged {amount} message(s)",color=discord.Color.green())
    await interaction.channel.send(embed=embed)

# command to set activity status of bot
@discord_bot.tree.command(name='botstatus',description='Sets Presence of Bot')
@app_commands.checks.has_any_role('Server Owner')
async def botstatus(interaction: discord.Interaction, status:str):
    await interaction.response.defer(ephemeral=True,thinking=True)
    statuslist = ['online','dnd','idle','offline','invisible']
    if status not in statuslist:
        await interaction.followup.send(f'Status **{status}** does not exist.')
    else:
        if status == 'online':
            await discord_bot.change_presence(status=discord.Status.online)
        if status == 'dnd':
            await discord_bot.change_presence(status=discord.Status.dnd)
        if status == 'offline':
            await discord_bot.change_presence(status=discord.Status.offline)
        if status == 'idle':
            await discord_bot.change_presence(status=discord.Status.idle)
        if status == 'invisible':
            await discord_bot.change_presence(status=discord.Status.invisible)
        await interaction.followup.send(f'Status was changed to **{status}**.')
        
"""
Trying to create a permission-issue command to let the user know he does not have enough permission to run the command he wanted to.
"""
# calling main function and printing out the errors from it.
if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        print(error)