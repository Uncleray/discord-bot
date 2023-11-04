# imports
import os

# read discord token from .env file
with open('.env', 'r') as file:
    lines = file.readlines()
    for line in lines:
        key, value = line.strip().split('=')
        if key == 'DISCORD_BOT_TOKEN':
            os.environ['DISCORD_BOT_TOKEN'] = value

# get the token from the environment variable
discord_api_secret = os.getenv('DISCORD_BOT_TOKEN')