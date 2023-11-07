import sys
from colorama import Back, Fore, Style
import platform
import time
import discord
from discord.ext import commands
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
@discord_bot.tree.command(name='ping', description='Will send a Pong back!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(content='Pong!')

# calling main function and printing out the errors from it.
if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        print(error)