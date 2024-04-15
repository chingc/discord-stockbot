import os

import discord

from server import keep_alive
from ticker import lookup


def help():
    return """StockBot Commands:
    **lookup (lu)**: Lookup a symbol.
        Prepend "^" for indexes.
        Append "=F" for futures.
            Examples:
                !stockbot lookup SPY
                !stockbot lookup ^SPX
                !stockbot lookup ES=F"""


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(client.user, "logged in")


@client.event
async def on_message(message):
    if message.content.startswith("!stockbot") and message.author != client.user:
        match message.content.split():
            case ["!stockbot", ("lookup" | "lu"), symbol]:
                await message.channel.send(lookup(symbol))
            case ["!stockbot"]:
                await message.channel.send(help())
            case _:
                pass


keep_alive()
client.run(os.environ["DISCORD_BOT_TOKEN"])
