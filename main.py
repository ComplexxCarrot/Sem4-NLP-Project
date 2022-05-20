import os
from discord_client import DiscordClient

client = DiscordClient()
client.run(os.environ['TOKEN'])


# my resources:
# https://www.youtube.com/watch?v=SPTfmiYiuok
# https://towardsdatascience.com/how-to-build-your-own-ai-chatbot-on-discord-c6b3468189f4
# https://stackoverflow.com/questions/61784710/make-discord-python-rewrite-bot-tag-message-author
# https://github.com/Digiwind/Digiwind-Videos/tree/main/Moderation%20Bot
# ^ for timeout + logging
# python3 -m pip install -U py-cord --pre
# py -3 -m pip install -U git+https://github.com/Pycord-Development/pycord