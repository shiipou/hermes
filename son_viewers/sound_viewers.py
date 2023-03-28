import random
import glob

from twitchio.ext import sounds

usersound = dict()

async def play(self, ctx, username):
    soundsList = usersound.get(username)
    if not soundsList:
        soundsList = []
        for file in glob.glob(f'son_viewers/{username}/*'):
            soundsList.append(sounds.Sound(source=file))
        usersound[username] = soundsList 
    if len(soundsList) != 0: 
        await ctx.send(f" captai1440Heyfree Bonjour {username} !")
        audio_player.play(random.choice(soundsList))


async def player_done():
    pass


audio_player = sounds.AudioPlayer(callback=player_done)