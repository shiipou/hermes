import random
# import requests
# import json

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


    # #meteo (spatial)
    # @commands.command()
    # @commands.cooldown(1, 120, commands.Bucket.user)
    # async def meteo(self, ctx):
    #     # Configuration de l'API de la NASA
    #     API_URL = "https://api.nasa.gov/DONKI/"
    #     ENDPOINT = "notifications?type=all&api_key=disfJjDgT7DMmaYBaLtdRPvzchdJIcUrH50FDGlD"

    #     # Appel à l'API de la NASA pour récupérer les informations
    #     response = requests.get(API_URL + ENDPOINT)
    #     data = response.json()


    #     # Récupération des informations
    #     solar_wind_speed = data[0]['solarWindSpeed']
    #     solar_wind_density = data[0]['solarWindDensity']
    #     x_ray_flux = data[0]['xrayFlux']
    #     kp_index = data[0]['kpIndex']
    #     message = f"Conditions météorologiques exterrieur à la station : vitesse du vent solaire = {solar_wind_speed} km/s, densité du vent solaire = {solar_wind_density} p/cm3, flux de rayons X = {x_ray_flux}, indice géomagnétique terrestre (Kp) = {kp_index}."

    #     # Envoi du message dans le chat Twitch
    #     await ctx.channel.send(message)

