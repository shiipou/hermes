import random
import glob

from pydub import AudioSegment, playback


usersound = dict()

sound_queue = []

async def play(self, ctx, username):
    soundsList = usersound.get(username)
    if not soundsList:
        soundsList = []
        for file in glob.glob(f'son_viewers/{username}/*'):
            soundsList.append(AudioSegment.from_file(file))
        usersound[username] = soundsList
    if len(soundsList) != 0:
        await ctx.send(f" captai1440Heyfree Bonjour {username} !")
        choice = random.choice(soundsList)
        loop = False
        if len(sound_queue) == 0:
            loop = True
        sound_queue.append({"username": username, "sound":choice})
        if loop:
            await loop_sounds(self)

async def loop_sounds(self):
    while len(sound_queue) > 0:
        item = sound_queue.pop(0)
        username = item["username"]
        sound = item["sound"]
        playback.play(sound)