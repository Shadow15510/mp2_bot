import discord
from discord.ext import commands, tasks
import json
import os

from bot.files.commands import MPCommands
from bot.files.cdp import get_cdp_rss


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
    cdp_implementation.start()
    print("Connecté.")

# Initialisation de la tâche
@tasks.loop(seconds=10)
async def cdp_implementation():
    rss = get_cdp_rss()
    channel = mp2_bot.get_channel(id=config["CDP_CHANNEL_ID"])

    if rss:
        for title, link in rss:
            embed = discord.Embed(title="Notification Cahier de Prépa", description="Un nouveau document a été mis en ligne", color=config["COLOR"])
            embed.add_field(name=title, value=link)
            await channel.send(embed=embed)
    else:
        await channel.send("RAS")

# Lancement du bot
mp2_bot.run(os.environ["token"])