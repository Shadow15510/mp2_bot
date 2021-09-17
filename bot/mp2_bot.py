import discord
from discord.ext import commands, tasks
import json
import os

from bot.files.commands import MPCommands


# Chargement du fichier de configuration
with open("bot/config.json", "r") as config_file:
    config = json.load(config_file)


# Création du bot
mp2_bot = commands.Bot(command_prefix=config["PREFIX"])
mp2_bot.add_cog(MPCommands(config))


# Initialisation du statut personalisé
@mp2_bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name=config["PREFIX"] + "aide")
    await mp2_bot.change_presence(activity=activity)
    cdp_implementation.sgtart()
    print("Connecté.")

# Initialisation de la tâche
@tasks.loop(seconds=5)
async def cdp_implementation():
    channel = mp2_bot.get_channel(id=config["CDP_CHANNEL_ID"])
    await channel.send("Message")

# Lancement du bot
mp2_bot.run(os.environ["token"])