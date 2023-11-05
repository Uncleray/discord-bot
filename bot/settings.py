# imports
import os
from dotenv import load_dotenv

load_dotenv()

# set value to variables from .env file
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PREFIX = os.getenv('DISCORD_BOT_PREFIX')
WELCOME_CHANNEL = os.getenv('DISCORD_WELCOME_CHANNEL')
GOODBYE_CHANNEL = os.getenv('DISCORD_GOODBYE_CHANNEL')