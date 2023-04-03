import random
import asyncio
import spacy
import datetime
import re
import openai
import twitchapi

from modules import event_message
from modules.chatGPT import chatgpt
from son_viewers import sound_viewers
from modules import commandes
from modules.games.games import Game as StoryGame
from modules.games.story import Story

from twitchio.ext import commands


filename = 'song'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
quiets = ["Eh Oh, reste polis hein !", "Je crois que ce martien veux communiquer", "Pardon?",
          "Il me semble que ceci est une indication pour me taire, mais seul le créateur du bot peux m'éteindre",]
nlp = spacy.load("en_core_web_sm")


# ----------------------------------------------------------------#
# Créez une instance de bot Twitch.
class Bot (commands.Bot):
    channels: str = None
    personnality: str = None
    channel_rules: str = None
    story_game: StoryGame = None

    def __init__(self):
        # charger le jeton et l'identifiant du client en utilisant une expression rationnelle à partir d'un fichier de cette forme : username=xxxxxx;user_id=xxxxxx;client_id=xxxxx;oauth_token=xxxx; or client_id=xxxxx \n oauth_token=xxxx
        with open('bot.config', 'r') as f:
            config = f.read() # ce qui permet de lire le contenu du fichier de configuration
            # il extrait le jeton oauth dans le fichier de configuration
            token_match = re.search(r'oauth_token=([a-z0-9]+)', config)
            # il extrait l'identifiant du client dans le fichier de configuration
            client_id_match = re.search(r'client_id=([a-z0-9]+)', config)

            # extraire les chaînes à écouter de ce format : channels=xxxxx,xxxxx,xxxxx
            listen_channels_match = re.search(
                r'channels=([a-zA-Z0-9_,]+)', config)
            openai_api_key_match = re.search(
                r'openai_api_key=([a-zA-Z0-9_\-,]+)', config)

        self.twitchApi = twitchapi.TwitchApi(
            client_id_match.group(1), token_match.group(1))
        with open('modules/chatGPT/personnality_rules.md', 'r') as f:
            self.personnality = f.read()
        with open('modules/chatGPT/channel_rules.md', 'r') as f:
            self.channel_rules = f.read()

        # gestion des erreurs si le token ou l'identifiant du client n'est pas trouvé dans le fichier bot.config
        if not token_match or not client_id_match:
            # Envoyer l'erreur au gestionnaire d'erreur (à la fin du fichier)
            raise ValueError(
                'Token ou identifiant client introuvable dans bot.config, vous pouvez les obtenir à partir de https://chatterino.com/client_login')

        if not listen_channels_match:
            # Envoyer l'erreur au gestionnaire d'erreur (à la fin du fichier)
            raise ValueError(
                'Canaux non trouvés dans bot.config, vous devez configurer le canal que vous voulez écouter.')
        self.channels = listen_channels_match.group(1).split(',')
        openai.api_key = openai_api_key_match.group(1)

        # initialise the bot
        super().__init__(token=token_match.group(1),
                         client_id=client_id_match.group(1),
                         nick='h_e_r_m_e_s__bot',
                         prefix='-',
                         # initial_channels    =['Captain_Marty_']),
                                initial_channels=self.channels
                         )
        self.add_cog(commandes.CommandsCog(self))

    async def event_ready(self):
        print('#----------------------------------------------------------------#')
        print(f'Bot allumer sous le nom | {self.nick}')
        print(f'Sur la chaîne de | Captain_Marty_')
        print(timestamp)
        print('#----------------------------------------------------------------#')
        await asyncio.gather(
            event_message.send_message_wakeup(self),
            event_message.send_message_info(self),
            event_message.send_message_talk(self),
            sound_viewers.loop_sounds(self),
        )

    # Message user du tchat

    async def event_message(self, message):
        if message.echo:
            return
        print(timestamp, message.author.name, ": ", message.content)

        # Regarde dans le message User si il contient  "troll" ou "chatgpt" ou "son du viewers"
        if message.author.name.lower() != self.nick.lower():
            if self.story_game is not None and self.story_game.player.lower() == message.author.name.lower():
                if self.story_game.story.max_player_interaction - len(self.story_game.story.adventures) <= 0:
                    await message.channel.send("Félicitation, vous avez terminé l'histoire ! Merci d'avoir joué !")
                    self.story_game = None
                    return
                msg = self.story_game.play(message.content)
                await message.channel.send(msg)
                return
            
            if f"@{self.nick.lower()}" in message.content.lower():
                await chatgpt.event_message_gpt(self, message)
            if f"-{message.author.name.lower()}" in message.content.lower():
                print(timestamp, message.author.name, ": son du viewers")
                await sound_viewers.play(self, message.channel, message.author.name.lower())
        await super().event_message(message)

    # story game
    @commands.command(name='start_game', aliases=['sg', 'story', 'game'])
    @commands.cooldown(1, 900, commands.Bucket.user)
    async def start_game(self, ctx):
        user = ctx.author.name

        if self.story_game is not None:
            if user.lower() == self.story_game.player.lower():
                await ctx.send(f"@{user}, désolé tu es déjà en train de jouer!")
                return
            
            await ctx.send(f"@{user}, désolé un jeu est déjà en cours. Attends ton tour!")
            return

        init_msg = ctx.message.content.split(' ', 1)[1]
        if (init_msg is None or init_msg == ''):
            ctx.send(f"@{user}, désolé, tu dois donner un context d'histoire!")
            return
        
        await ctx.send(f"Attends je met ça en place pour toi {user} !")
        self.story_game = StoryGame(user, Story(15, init_msg))
        game_init_message = self.story_game.start()
        await ctx.send(game_init_message)

 # ----------------------------------------------------------------#


if __name__ == "__main__":
    # try catch (catch s'appel except en python) pour gérer les erreurs connues sur le bot qui doivent ici arrêter l'execution du bot
    try:
        bot = Bot()
        bot.run()
    except KeyboardInterrupt:
        print("Bot arrêté par l'utilisateur")
    except ValueError as e:
        print(f'Error: {e}')
