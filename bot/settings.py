# imports
import os
from dotenv import load_dotenv

load_dotenv()

# set value to variables from .env file
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PREFIX = os.getenv('DISCORD_BOT_PREFIX')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')