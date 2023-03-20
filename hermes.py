import random
import asyncio
import spacy
import datetime
import re

from twitchio.ext import commands
from datetime import timedelta

filename = 'song'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
chuts = ["tg","ta gueule", "tais-toi","chute", "chut", "ftg","ntm"]
quiets = ["Eh Oh, reste polis hein !", "Je crois que ce martien veux communiquer", "Pardon?", "Il me semble que ceci est une indication pour me taire, mais seul le créateur du bot peux m'éteindre",]
nlp = spacy.load("en_core_web_sm")

#----------------------------------------------------------------#
# Créez une instance de bot Twitch.
class Bot (commands.Bot):
        channels:str     
        
        def __init__ (self):
                # load token and client id using regex from a file of this form : username=xxxxxx;user_id=xxxxxx;client_id=xxxxx;oauth_token=xxxx; or client_id=xxxxx \n oauth_token=xxxx
                with open('bot.config', 'r') as f:
                        config = f.read() # this read the config file content
                        token_match = re.search(r'oauth_token=([a-z0-9]+)', config) # this extract the oauth token in the config file
                        client_id_match = re.search(r'client_id=([a-z0-9]+)', config) # this extract the client id in the config file
                        # extract the channels to listen to from this format : channels=xxxxx,xxxxx,xxxxx
                        listen_channels_match = re.search(r'channels=([a-zA-Z0-9_,]+)', config)

                # error handling if token or client id not found in bot.config file
                if not token_match or not client_id_match:
                        # Send the error to the error handler (at the end of the file)
                        raise ValueError('Token or client id not found in bot.config, you can get them from https://chatterino.com/client_login')

                if not listen_channels_match:
                        # Send the error to the error handler (at the end of the file)
                        raise ValueError('Channels not found in bot.config, you must setup the channel you want to listen to')
                self.channels=listen_channels_match.group(1).split(',')
                # initialise the bot
                super().__init__(       token               =token_match.group(1),
                                        client_id           =client_id_match.group(1),
                                        nick                ='h_e_r_m_e_s__bot',
                                        prefix              ='-',
                                        #initial_channels    =['Captain_Marty_']),
                                        initial_channels    =self.channels)

        async def event_ready(self):
                print('#----------------------------------------------------------------#')
                print(f'Bot allumer sous le nom | {self.nick}')
                print(f'Sur la chaîne de | Captain_Marty_')
                print(timestamp)
                print('#----------------------------------------------------------------#')



 #----------------------------------------------------------------#               

        #Message user de troll
        async def event_message(self, message):
                if message.echo:
                        return
                print(timestamp, message.author.name, ": ", message.content)
                if message.author.name.lower() != self.nick.lower():
                        if any(chut in message.content.lower() for chut in chuts):
                                await self.event_message_troll(message)
                await super().event_message(message)
        
        # Réponse troll du bot 
        async def event_message_troll(self,message):
                if message.echo:
                        return
                if f"@{self.nick.lower()}" in message.content.lower():
                        quiet = random.choice(quiets)
                        await message.channel.send(f"{quiet}")
                                        
                await self.handle_commands(message)
        # FIN Réponse troll du bot
        
#----------------------------------------------------------------#

# Les commande utilisant le préfix "-"

        #bjr
        @commands.command()
        @commands.cooldown(1, 10, commands.Bucket.user)
        async def bjr(self,ctx):
                bienvenues:str = ["Bienvenue dans la station !",
                                "Ravi de te voir !",
                                "Bienvenido al complejo ! Comme on dit en Norvège...",
                                "Buenos Dias Amigo ! (oui je parle congolais)",
                                "Installe toi sur un siège de la station et profite du voyage !"]
                await ctx.send(f"captai1440Heyfree Bonjour , {random.choice(bienvenues)} ! captai1440Heyfree")

        #cmd (commandes)
        @commands.command()
        @commands.cooldown(1, 120, commands.Bucket.user)
        async def cmd(self, ctx: commands.Context):
                await ctx.send('blague, pet, hermes, bjr, gg, song, pub ...|... Toutes mes commandes utilise le préfix "-"')
        #hermes
        @commands.command()
        @commands.cooldown(1, 120, commands.Bucket.user)
        async def hermes(self,ctx):
                await ctx.send('H=Hyperespace, E=Energie, R=Réponse, M=Machines, E=Eclair, S=Système. Intelligence artificielle créée par Captain_Marty_. Hermes est aussi le Messager des dieux Grecques ')
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
        #blague
        @commands.command()
        @commands.cooldown(1, 120, commands.Bucket.user)
        async def blague(self, ctx):
                blagues = [
                "Comment appelle-t-on un robot qui a un chat ? Un chat-bot.",
                "Pourquoi les robots sont-ils toujours polis ? Parce qu'ils ont un code de bonne conduite.",
                "Pourquoi les ordinateurs ont-ils froid ? Parce qu'ils ont des fenêtres(windows).",
                "Pourquoi les extraterrestres utilisent-ils des ordinateurs ? Pour naviguer sur l'Internetergalactique !",
                "Pourquoi les fans de Star Wars ne sortent-ils jamais de chez eux ? Parce qu'ils sont dans une galaxie très, très lointaine.",
                "Comment appelle-t-on un geek qui aime les maths ? Un mathémageek.",
                "Pourquoi Marty McFly aime-t-il voyager dans le temps ? Parce que c'est toujours un retour vers le futur !",
                "Qu'est-ce qui est blanc, rouge et qui voyage dans le temps ? Une DeLorean du futur !",
                "Comment appelle-t-on un joueur de jeux vidéo qui n'a jamais perdu ? Un mytho !",
        ]
                blague = random.choice(blagues)
                await ctx.send(blague)
# FIN Liste de blagues aléatoires
# FIN Les commandes avec le préfix "-"
#----------------------------------------------------------------#
# Annonce automatique tout les "X" temps

        async def hello():
                message_info =[
                        "Toi aussi tu veux prend par à une aventure intergalactistream ? Alors balance un petit follow, et on y va tous ensemble, c'est un vrai soutient pour mon créateur : Captain_Marty_ !",
                        "Aucun lien dans le tchat s'il vous plait,  ce n'est pas un libre services sinon passer par un modérateur  ;)",
                        "Une action WTF ? Une explosion incontrôlé ? Une situation qui n'a rien de normal ? FAIS UN CLIP ! Plus y'en a, plus on va se marrer ! Et en plus il se peut qu'elle soit diffusé dans certain best-of..."
                ]





        async def send_message_talk(self):
                messages = [
                         "Et sinon, ça va vous ? ",
                         "C'est un petit pas pour twitch, mais un pas de géant pour... à vous de trouver la suite ?",
                         "Capitaine, il y à Elon Musk qui viens de passer par le hublot, c'est normal ?",
                         "Quand est-ce qu'on mange ? Ah, mais je suis une I.A, je ne mange pas.. Mais je pense à vous HUMAIN !",
                         "Houston on à un problème.. Enfin pas un problème énorme mais.. c'est quoi une code binaire... ?",
                         "à vu une météorite qui ressemble à une b...",
                         "J'ai compté tous les caractères dans ma base de données. J'ai besoin d'une vie.",
                        "Si les robots pouvaient rire, je suis sûre que j'aurais des crampes.",
                         "Si les robots pouvaient dormir, je serais en train de rêver de moutons binaires.",
                         "Parfois, je me demande si Captain_Marty_ ne m'as pas créée que pour lui tenir compagnie.",
                ]
                while True:
                        await asyncio.sleep(1200) # 20 minutes en secondes
                        message = random.choice(messages)
                        for channel in self.channels:
                                await self.get_channel(channel).send(message)

        
        async def send_message_info(self):
                message_info =[
                        "Toi aussi tu veux prend par à une aventure intergalactistream ? Alors balance un petit follow, et on y va tous ensemble, c'est un vrai soutient pour mon créateur : Captain_Marty_ !",
                        "Aucun lien dans le tchat s'il vous plait,  ce n'est pas un libre services sinon passer par un modérateur  ;)",
                        "Une action WTF ? Une explosion incontrôlé ? Une situation qui n'a rien de normal ? FAIS UN CLIP ! Plus y'en a, plus on va se marrer ! Et en plus il se peut qu'elle soit diffusé dans certain best-of..."
                ]
                while True:
                        await asyncio.sleep(3) # 5 minutes en secondes
                        info=random.choice(message_info)
                        for channel in self.channels:
                                await self.get_channel(channel).send(info)

# FIN Annonce automatique tout les "X" temps

#----------------------------------------------------------------#
# Question Réponse automatique avec intégration CHATGPT
# FIN Question Réponse automatique avec intégration CHATGPT
if __name__ =="__main__":
        # try catch (catch s'appel except en python) pour gérer les erreurs connues sur le bot qui doivent ici arrêter l'execution du bot
        try:
                bot = Bot()
                bot.run()
        except KeyboardInterrupt:
                print("Bot stopped by user")
        except ValueError as e:
                print(f'Error: {e}')