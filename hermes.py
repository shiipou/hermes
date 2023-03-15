import random
import asyncio
import spacy
import datetime
import re



from twitchio.ext import commands
from datetime import timedelta

filename = 'song'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
salutations = ["bonjour", "salut", "hey", "coucou", "yo", "wesh", "Salutation", "Bonjour", "Salut", "Hey", "Coucou","Yo", "Wesh", "salutation"]
chut = ["tg","ta gueule", "tais-toi","chute", "chut", "ftg","ntm"]
nlp = spacy.load("en_core_web_sm")


#----------------------------------------------------------------#

# Créez une instance de bot Twitch.
class Bot (commands.Bot):
        def __init__ (self):
                # load token and client id using regex from a file of this form : token=oauth:1234567890abcdefg client_id=1234567890abcdefg
                with open('bot.config', 'r') as f:
                        config = f.read()
                        token = re.search(r'token=(\S+)', config).group(1)
                        client_id = re.search(r'client_id=(\S+)', config).group(1)

                # error handling if token or client id not found in bot.config file
                if not token or not client_id:
                        raise ValueError('Token or client id not found in bot.config, you can get them from https://chatterino.com/client_login')

                # initialise the bot
                super().__init__(       token               =token,
                                        client_id           =client_id,
                                        nick                ='h_e_r_m_e_s__bot',
                                        prefix              ='-',
                                        initial_channels    =['shiishii_labs'])

        async def event_ready(self):
                print('#----------------------------------------------------------------#')
                print(f'Bot allumer sous le nom | {self.nick}')
                print(f'Sur la chaîne de | Captain_Marty_')
                print(timestamp)
                print('#----------------------------------------------------------------#')
                # await self.send_message()


        #Message de bienvenue
        async def event_message(self, message):

                ### code original :
                # if message.echo:
                #        return
                #
                # print(message.content)
                # if message.author.name.lower() != self.nick.lower():
                #         content_words = message.content.lower().split()
                #         for word in content_words:
                #                 if re.match(r'\b({})\b'.format('|'.join(salutations)), word):
                #                         bienvenue = random.choice(bienvenues)
                #                         await message.channel.send(f"Bonjour {message.author.name} {bienvenue}")
                #                         break
                ###

                # Ignorer les messages du bot lui-même
                if message.author.name.lower() != self.nick.lower():
                        ## Vérifier si le message contient une salutation
                        # Pour expliquer ce code, je vais utiliser un exemple :
                        # message.content = "Bonjour, je m'appelle John"
                        # salutations = ["bonjour", "salut", "hey", "coucou", "yo", "wesh", "Salutation", "Bonjour", "Salut", "Hey", "Coucou","Yo", "Wesh", "salutation"]
                        #
                        # 1. On transforme le message en minuscule
                        # 2. On parcours la liste des salutations
                        # 3. On vérifie si la salutation en cours est dans le message
                        # 3. Si oui, on envoie un message de bienvenue
                        if any(salutation in message.content.lower() for salutation in salutations):
                                self.event_message_welcome(message)

                await super().event_message(message)

        async def event_message_welcome(self, message: str):
                """
                Envoie un message de bienvenue quand les viewers salut le tchat
                """
                bienvenues = ["Bienvenue dans la station !",
                                "Ravi de te voir !",
                                "bienvenido al complejo ! Comme on dit en Norvège...",
                                "installe toi sur un siège de la station et profite du voyage !"]
                bienvenue = random.choice(bienvenues)
                await message.channel.send(f"Bonjour {message.author.name} {bienvenue}")
        # FIN Message de bienvenue quand les viewers salut le tchat

        # Message pour dire au bot de se taire (troll)
        async def event_message_troll(self,message):
                quiets = ["Eh Oh, reste polis hein !",
                         "Je crois que ce martien veux communiquer",
                         "Pardon?",
                         "Il me semble que ceci est une indication pour me taire, mais seul le créateur du bot peux m'éteindre",]
                print(message.content)

                if message.echo:
                        return

                if f"@{self.nick.lower()}" in message.content.lower():
                        content_words = message.content.lower().split()
                        for word in content_words:
                                if re.match(r'\b({})\b'.format('|'.join(chut)), word):
                                        quiet = random.choice(quiets)
                                        await message.channel.send(f"{quiet}")
                                        break

                await self.handle_commands(message)
        # FIN Message pour dire au bot de se taire (troll)

#----------------------------------------------------------------#

# Les commande utilisant le préfix "-"

        #Bonjour
        @commands.command()
        @commands.cooldown(1, 120, commands.Bucket.user)
        async def bonjour(self, ctx: commands.Context):
                await ctx.send(f'Bonjour {ctx.author.name}!')

        #cmd (commandes)
        @commands.command()
        @commands.cooldown(1, 120, commands.Bucket.user)
        async def cmd(self, ctx: commands.Context):
                await ctx.send('blague, pet, hermes, bonjour, gg, song, pub ...|... Toutes mes commandes utilise le préfix "-"')

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


        #blagues
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
        async def send_message(self):
                messages = [
                        "Et sinon, ça va vous ? ",
                        "C'est un petit pas pour twitch, mais un pas de géant pour... à vous de trouver la suite ?",
                        "Capitaine, il y à Elon Musk qui viens de passer par le hublot, c'est normal ?",
                        "Quand est-ce qu'on mange ? Ah, mais je suis une I.A, je ne mange pas.. Mais je pense à vous HUMAIN !",
                        "Houston on à un problème.. Enfin pas un problème énorme mais.. c'est quoi une code binaire... ?",
                        "à vu une météorite qui ressemble à une b...",
                        "J'ai compté tous les caractères dans ma base de données. J'ai besoin d'une vie.",
                        "Si les robots pouvaient rire, je suis sûre que j'aurais des crampes.",
                        "Je m'ennuie tellement que je suis en train de compter les pixels de mon écran. Et en plus, j'ai pas d'écran...",
                        "Si les robots pouvaient dormir, je serais en train de rêver de moutons binaires.",
                        "Parfois, je me demande si Captain_Marty_ ne m'as pas créée que pour lui tenir compagnie.",
                        "Toi aussi tu veux prend par à une aventure intergalactistream ? Alors balance un petit follow, et on y va tous ensemble, c'est un vrai soutient pour mon créateur : Captain_Marty_ !",
                        "Aucun lien dans le tchat s'il vous plait,  ce n'est pas un libre services sinon passer par un modérateur  ;)",
                        "Une action WTF ? Une explosion incontrôlé ? Une situation qui n'a rien de normal ? FAIS UN CLIP ! Plus y'en a, plus on va se marrer ! Et en plus il se peut qu'elle soit diffusé dans certain best-of..."
                ]
                while True:
                        message = random.choice(messages)
                        await self.get_channel('Captain_Marty_').send(message)
                        await asyncio.sleep(900) # 15 minutes en secondes

 # 10 minutes en secondes
# FIN Annonce automatique tout les "X" temps

#----------------------------------------------------------------#

# Question Réponse automatique avec intégration CHATGPT


# FIN Question Réponse automatique avec intégration CHATGPT
if __name__ =="__main__":
        bot = Bot()
        bot.run()
