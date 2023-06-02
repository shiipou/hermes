import random
import requests
import json
import twitchio


from twitchio.ext import commands
from son_viewers import sound_viewers

class commandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #bjr
    @commands.command()
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def bjr(self,ctx):
            bienvenues:str = ["Bienvenue dans la station !",
                            "Ravi de te voir !",
                            "Bienvenido al complejo ! Comme on dit en Norvège...",
                            "Buenos Dias Amigo ! (oui je parle Islandais)",
                            "Installe toi sur un siège de la station et profite du voyage !"]
            await ctx.send(f"captai1440Heyfree Bonjour , {random.choice(bienvenues)} ! captai1440Heyfree")

    #bye
    @commands.command()
    @commands.cooldown(1, 10, commands.Bucket.user)
    async def bye(self,ctx):
            bienvenues:str = ["A bientôt !",
                            "Au revoir, merci de ton soutient !",
                            "Adios Amigos dé la stazionné",
                            "Orvoèèère ! "]
            await ctx.send(f"captai1440Heyfree {random.choice(bienvenues)} ! captai1440Heyfree")

    #cmd (commandes)
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def cmd(self, ctx: commands.Context):
            await ctx.send(', bjr, bye, gg, song, pub, pet ...|... Toutes mes commandes utilise le préfix "-"')

    #pet
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def pet(self,ctx):
            await ctx.send(f"Désolé {ctx.author.name}, je suis une intelligence artificielle et je ne suis pas capable de faire des flatulences (pour le moment). Peut-être que vous pourriez essayer de trouver une blague plus appropriée ?")

    #gg
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def gg(self,ctx):
            await ctx.send(f"CLAP CLAP CLAP ! ... C'est comme ça qu'on fais ?")

    #pub
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def pub(self,ctx):
            await ctx.send(f"Regarde en dessous de la fenêtre de stream {ctx.author.name} tu retrouveras tous mes réseaux sociaux !")

    #help
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def help(self,ctx):
            await ctx.send(f"Pour me demander de l'aide, utilise la commande 'sos' + [ton message], pense à bien décrire, c'est important! ")


    #music en cours avec une lecture de fichier ".txt"
    #song
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def song(self,ctx):
            filename = 'song.txt'
            with open(filename, "r") as file:
                    content = file.read()
            message = "Voici la musique en cours : " + content
            await ctx.send(message)

    #playAd  (son des viewers de secours par l'Admin)
    @commands.command()
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def playAd(self, ctx: commands.Context, *, username: str) -> None:
            #track = await sounds.Sound.ytdl_search(username)
            #self.music_player.play(track)
            if ctx.author.is_broadcaster:
                await sound_viewers.play(self, ctx, username)

    #ETS2 Mod
    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def etsmod(self,ctx):
            await ctx.send(f"Voici les mods que j'utilise : https://docs.google.com/spreadsheets/d/1bhOgikyoc-ZcrD4imM6rCCw1MnMfJsDP0KU7QdIf1MM/edit?usp=sharing")
  

    #titre
    @commands.command()
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def titre(self, ctx):
        mots_cles1 = [
            "La galaxie",
            "Les explorateurs",
            "L'aventure",
            "Les Denis",
            "Le voyage",
            "Les voyages",
            "La planète",
            "Les astéroïdes",
            "Les vaisseaux",
            "Area",
            "Hermes"
            ]
        mots_cles2 = [
            "perdu",
            "seul",
            "désanchanté",
            "renouveaux",
            "enchanté",
            "libre",
            "intriguant",
            "dangereux",
            "destiné",
            "58",
            "62"
        ]
        await ctx.send(f"{random.choice(mots_cles1)} {random.choice(mots_cles2)}")