import sys
import discord
from discord.ext import commands
import settings

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

# calling main function and printing out the errors from it.
if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        print(error)