import discord
from discord.ext import commands
import json
import os

from bot.files.commands import MPCommands


# Chargement du fichier de configuration
with open("bot/config.json", "r") as config_file:
    config = json.load(config_file)


# Création du bot
mp2_bot = commands.Bot(command_prefix=config["PREFIX"], description="Bot de la MP 2")
mp2_bot.add_cog(MPCommands(config))


@mp2_bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name=config["PREFIX"] + "aide")
    await mp2_bot.change_presence(activity=activity)
    print("Connecté.")


# Lancement du bot
mp2_bot.run(os.environ["token"])