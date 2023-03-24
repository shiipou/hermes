import random
import asyncio
import spacy
import datetime
import re
import openai
import twitchapi


from twitchio.ext import commands
from datetime import timedelta


filename = 'song'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
chuts = ["tg","ta gueule", "tais-toi","chute", "chut", "ftg","ntm"]
quiets = ["Eh Oh, reste polis hein !", "Je crois que ce martien veux communiquer", "Pardon?", "Il me semble que ceci est une indication pour me taire, mais seul le créateur du bot peux m'éteindre",]
nlp = spacy.load("en_core_web_sm")
wakeup_message = 'Je viens de me réveiller! Je suis prêt à vous divertir pour le stream !'


#----------------------------------------------------------------#
# Créez une instance de bot Twitch.
class Bot (commands.Bot):
        channels:str
        personnality:str
        channel_rules:str
       
        def __init__ (self):
                # load token and client id using regex from a file of this form : username=xxxxxx;user_id=xxxxxx;client_id=xxxxx;oauth_token=xxxx; or client_id=xxxxx \n oauth_token=xxxx
                with open('bot.config', 'r') as f:
                        config = f.read() # this read the config file content
                        token_match = re.search(r'oauth_token=([a-z0-9]+)', config) # this extract the oauth token in the config file
                        client_id_match = re.search(r'client_id=([a-z0-9]+)', config) # this extract the client id in the config file
                        # extract the channels to listen to from this format : channels=xxxxx,xxxxx,xxxxx
                        listen_channels_match = re.search(r'channels=([a-zA-Z0-9_,]+)', config)
                        openai_api_key_match = re.search(r'openai_api_key=([a-zA-Z0-9_\-,]+)', config)

                self.twitchApi=twitchapi.TwitchApi(client_id_match.group(1),token_match.group(1))
                with open('personnality_rules.md', 'r') as f:
                        self.personnality = f.read()
                with open('channel_rules.md', 'r') as f:
                        self.channel_rules = f.read()
                # error handling if token or client id not found in bot.config file
                if not token_match or not client_id_match:
                        # Send the error to the error handler (at the end of the file)
                        raise ValueError('Token or client id not found in bot.config, you can get them from https://chatterino.com/client_login')

                if not listen_channels_match:
                        # Send the error to the error handler (at the end of the file)
                        raise ValueError('Channels not found in bot.config, you must setup the channel you want to listen to')
                self.channels=listen_channels_match.group(1).split(',')
                openai.api_key=openai_api_key_match.group(1)
                # initialise the bot
                super().__init__(       token               =token_match.group(1),
                                        client_id           =client_id_match.group(1),
                                        nick                ='h_e_r_m_e_s__bot',
                                        prefix              ='-',
                                        #initial_channels    =['Captain_Marty_']),
                                        initial_channels    =self.channels
                                ),

        async def event_ready(self):
                print('#----------------------------------------------------------------#')
                print(f'Bot allumer sous le nom | {self.nick}')
                print(f'Sur la chaîne de | Captain_Marty_')
                print(timestamp)
                print('#----------------------------------------------------------------#')
                await asyncio.gather(
                        self.send_message_wakeup(),
                        self.send_message_info(),
                        self.send_message_talk(),
                )
                  
 #----------------------------------------------------------------# 
#Intégration chatGPT

        def generate_response(self, message, channel_settings):
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[  {"role": "system", "content": self.personnality},
                                {"role": "system", "content": channel_settings},
                                {"role": "user", "content": message.content},
                        ],
                    max_tokens=150,
                    n=1,
                    stop=None,
                    temperature=1.2,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                response = completion.choices[0].message.content.strip()
                return response
        
        async def event_message_gpt(self,message):
                stream_info = self.twitchApi.stream_info('Captain_Marty_')
                game_name='offline'
                title='offline'
                try:
                        game_name = stream_info[0].game_name
                        title = stream_info[0].title
                except:
                        pass
                channel_info = {
                        'channel_name': 'Captain_Marty_',
                        'channel_stream_title': title,
                        'channel_stream_category': game_name
                }
                channel_settings = f'{self.channel_rules}'

                for k, v in channel_info.items():
                        channel_settings = channel_settings.replace('{{' + k + '}}', str(v))

                # channel_info = await self.twitchApi.channel_info('Captain_Marty_')
                response = self.generate_response(message, channel_settings)
                print(timestamp, self.nick, ": ", response)
                await message.channel.send(f"{response}")

#FIN Intégration chatGPT
 #----------------------------------------------------------------#               

        #Message user du tchat
        async def event_message(self, message):
                if message.echo:
                        return
                print(timestamp, message.author.name, ": ", message.content)

                #Regarde dans le message User si il contient  "troll" ou "chatgpt"
                if message.author.name.lower() != self.nick.lower():
                        if any(chut in message.content.lower() for chut in chuts):
                                await self.event_message_troll(message)
                        if f"@{self.nick.lower()}" in message.content.lower():
                                await self.event_message_gpt(message)
                await super().event_message(message)

        #Réponse troll du bot 
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
                await ctx.send('blague, pet, bjr, bye, gg, song, pub ...|... Toutes mes commandes utilise le préfix "-"')
            
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

        #param
        @commands.command()
        @commands.cooldown(1, 60, commands.Bucket.user)
        async def param(self, ctx):
                params = [
                        "Honnêteté : 90%. L'honnêteté absolue n'est pas toujours la forme de communication la plus diplomatique ni la plus sûre avec les êtres émotionnels.",
                        "Humour 75% : Séquence d'arrêt du stream dans T moins 10, 9,... Comment ça on met 60% maintenant ?",
                        "Compassion 80% : Même si je suis une I.A, je me sent d'amitié pour vous :)",
                        "Confiance 30% : Plus bas que le vôtre envers moi, apparemment..",
                        "Technique 100% : Inutile de me demander, vous devriez le savoir ! (nameoh)",
                ]
                param = random.choice(params)
                await ctx.send(param)
# FIN Les commandes avec le préfix "-"

#----------------------------------------------------------------#

# Annonce automatique tout les "X" temps
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
                        "Aucun lien dans le tchat s'il vous plait, ce n'est pas un libre services sinon passer par un modérateur  ;)",
                        "Une action WTF ? Une explosion incontrôlé ? Une situation qui n'a rien de normal ? FAIS UN CLIP ! Plus y'en a, plus on va se marrer ! Et en plus il se peut qu'il soit diffusé dans certain best-of..."
                ]
                while True:
                        await asyncio.sleep(360) # 6 minutes en secondes
                        info=random.choice(message_info)
                        for channel in self.channels:
                                await self.get_channel(channel).send(info)

# FIN Annonce automatique tout les "X" temps
        async def send_message_wakeup(self):
                for channel in self.channels:
                        await self.get_channel(channel).send(wakeup_message)
#----------------------------------------------------------------#

if __name__ =="__main__":
        # try catch (catch s'appel except en python) pour gérer les erreurs connues sur le bot qui doivent ici arrêter l'execution du bot
        try:
                bot = Bot()
                bot.run()
        except KeyboardInterrupt:
                print("Bot stopped by user")
        except ValueError as e:
                print(f'Error: {e}')