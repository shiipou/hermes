import asyncio
import spacy
import datetime
import re
import openai
import twitchapi

from modules import event_message
from modules.chatGPT import chatgpt
from modules import commandes
from son_viewers import sound_viewers
from modules.games.games import Game as StoryGame
from modules.games.story import Story

from twitchio.ext import commands


filename = 'song'
timestamp = datetime.datetime.now().strftime("%d-%m-%Y -- %H:%M:%S")
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
            config = f.read()  # ce qui permet de lire le contenu du fichier de configuration
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
        super().__init__(   token=token_match.group(1),
                            client_id=client_id_match.group(1),
                            nick='h_e_r_m_e_s__bot',
                            prefix='-',
                            # initial_channels    =['Captain_Marty_']),
                            initial_channels=self.channels
                         ),
        self.add_cog(commandes.commandsCog(self))

    async def event_ready(self):
        print('#----------------------------------------------------------------#')
        print(f'Bot allumer sous le nom | {self.nick}')
        print(f'Sur la chaîne de | Captain_Marty_')
        print(f'Date, Heure : {timestamp}')
        print('#----------------------------------------------------------------#')
        await asyncio.gather(
            event_message.send_message_wakeup(self),
            event_message.send_message_info(self),
            event_message.send_message_talk(self),
        )

    # Message user du tchat

    async def event_message(self, message):
        if message.echo:
            return
        print(timestamp, message.author.name, ": ", message.content)

        # Regarde dans le message User si il contient "chatgpt" ou "son du viewers"
        if message.author.name.lower() != self.nick.lower():
            if self.story_game is not None and self.story_game.player.lower() == message.author.name.lower():
                if self.story_game.story.max_player_interaction - self.story_game.story.player_interaction <= 0:
                    await message.channel.send("Félicitation, vous avez terminé l'histoire ! Merci d'avoir joué !")
                    self.story_game = None
                    return
                msg = self.story_game.play(message.content)
                await self.send_message(message.channel, msg)
                return
            if f"@{self.nick.lower()}" in message.content.lower():
                await chatgpt.event_message_gpt(self, message)
            if f"-{message.author.name.lower()}" in message.content.lower():
                print(timestamp, message.author.name, ": son du viewers")
                await sound_viewers.play(self, message.channel, message.author.name.lower())
        await super().event_message(message)

    # Send message to chat
    async def send_message(self, channel, message):
        # split the message into multiple messages using regex if it's more than 450 characters
        messages = re.findall(r'.{1,450}(?:\s|$)', message)
        print(messages)
        for msg in messages:
            await channel.send(msg)
        return

    # story game
    @commands.command(name='start_game', aliases=['sg', 'story', 'game', 'sos'])
    @commands.cooldown(1, 300, commands.Bucket.user)
    async def start_game(self, ctx):
        user = ctx.author.name

        if self.story_game is not None:
            if user.lower() == self.story_game.player.lower():
                await ctx.send(f"@{user}, désolé ta demande d'aide est déjà pris en compte.")
                return

            await ctx.send(f"@{user}, désolé une demande d'aide est déjà en cours d'utilisation.")
            return

        init_msg = ctx.message.content.split(' ', 1)[1]
        if (init_msg is None or init_msg == ''):
            ctx.send(
                f"@{user}, désolé, je n'ai pas compris votre demande, veuillez reformuler.")
            return

        await ctx.send(f"Instruction reçu {user} je vais m'occuper de vous. Veuillez patientez le temps que je traite votre demande.")
        self.story_game = StoryGame(user, Story(15, init_msg))
        game_init_message = self.story_game.start()
        await self.send_message(ctx, game_init_message)

 # ----------------------------------------------------------------#


if __name__ == "__main__":
    nick = 'h_e_r_m_e_s__bot'
    # try catch (catch s'appel except en python) pour gérer les erreurs connues sur le bot qui doivent ici arrêter l'execution du bot
    try:
        bot = Bot()
        bot.run()
    except KeyboardInterrupt:
        print(f'Le bot : {nick} , est stoppé par l\'utilisateur')
    except ValueError as e:
        print(f'Error: {e}')