import discord
import json
import os

from discord.ext import commands

with open('config.json', mode='r', encoding='utf8') as config:
    c = json.load(config)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=c['prefix'], intents=intents)

@bot.event
async def on_ready():
    print('Bot is online!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(c['token'])