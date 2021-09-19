import discord
from discord.ext import commands
import sqlite3
from random import choice


class MPCommands(commands.Cog):
    def __init__(self, config, quotes):
        self.prefix = config["PREFIX"]
        self.color = config["COLOR"]

        self.quotes = quotes

    @commands.command(help="Afficher les commandes disponibles. Préciser un nom de commande renvoie l'aide détaillée.", brief="Affiche ce panneau")
    async def aide(self, ctx, cmnd: str=None):

        def get_syntax(cmnd):
            syntax = f"`{self.prefix}{cmnd.name}"

            for arg in cmnd.clean_params:
                if "=" in str(cmnd.clean_params[arg]): syntax+= f" [{arg}]"
                else: syntax += f" <{arg}>"

            return syntax + "`"

        if cmnd:
            embed = discord.Embed(title="Aide détaillée", description="Informations complémentaires", color=self.color)
            cmnd_data = {cmnd.name: cmnd for cmnd in self.get_commands()}

            if cmnd in cmnd_data:
                cmnd = cmnd_data[cmnd]
                embed.add_field(name="Syntaxe", value=get_syntax(cmnd), inline=True)
                embed.add_field(name="Description", value=cmnd.help, inline=True)
            else:
                embed.add_field(name="Erreur : commande inconnue", value=f"Entrez `{self.prefix}aide` pour avoir la liste des commandes.")
        
        else:
            embed = discord.Embed(title="Rubrique d'aide", description=f"Entrez : `{self.prefix}aide <commande>` pour plus d'informations sur une commande.\nLes arguments entre `<>` sont obligatoires.\nLes arguments entre `[]` sont facultatifs.", color=self.color)
            for cmnd in self.get_commands():
                embed.add_field(name=cmnd.brief, value=get_syntax(cmnd), inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Donne le ou les adresse(s) mail(s) selon une recherche. Si aucun mot-clef de recherche n'est donné, la commande retourne toutes les adresses mails connues.", brief="Retrouver une adresse mail")
    async def mail(self, ctx, *recherche):
        recherche = " ".join(recherche)

        if recherche:
            mail_bdd = sqlite3.connect("bot/files/mails.db")
            cursor = mail_bdd.cursor()

            result = cursor.execute(f"""
                SELECT nom, adresse FROM professeurs
                JOIN mails ON mails.prof_id = professeurs.id
                WHERE professeurs.patterns LIKE '%{recherche.lower()}%'
                """).fetchall()
            mail_bdd.close()

        else:
            mail_bdd = sqlite3.connect("bot/files/mails.db")
            cursor = mail_bdd.cursor()

            result = cursor.execute("""
                SELECT nom, adresse FROM professeurs
                JOIN mails ON mails.prof_id = professeurs.id
                """).fetchall()
            mail_bdd.close()

        if result:
            mails = {}
            for name, address in result:
                if name in mails: mails[name].append(address)
                else: mails[name] = [address]

            if recherche: embed = discord.Embed(title="Mail", description=f"Adresse(s) mail(s) correspondant à la recherche : '{recherche}'", color=self.color)
            else: embed = discord.Embed(title="Mail", description=f"Adresses mails connues", color=self.color)
            
            for name in mails:
                embed.add_field(name=name, value="\n".join([f"`{address}`" for address in mails[name]]), inline=False)

        else:
            embed = discord.Embed(title="Mail", description="Aucune addresse mail trouvée.", color=16711680)
            embed.add_field(name="Erreur", value="Aucune adresse mail ne correspond à la recherche effectuée.", inline=False)

        await ctx.send(embed=embed)

    @commands.command(help="Renvoie une citation de M. Le Duff au hasard", brief="Citation de M. Le Duff")
    async def citation(self, ctx):
        await ctx.send(f"> {choice(self.quotes)}")


