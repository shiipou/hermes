
import openai

from modules.games.story import Story

import os

PLAYER_MAX_INTERACTION = 15
PLAYER_MAX_INTERACTION_PROMPT: str = None
GENERATE_STORY_PROMPT: str = None
GENERATE_ADVENTURE_PROMPT: str = None
with open(f'{os.path.abspath(os.curdir)}/modules/games/templates/generate_story.md', 'r') as f:
    GENERATE_STORY_PROMPT = f.read()
with open(f'{os.path.abspath(os.curdir)}/modules/games/templates/generate_adventure.md', 'r') as f:
    GENERATE_ADVENTURE_PROMPT = f.read()
with open(f'{os.path.abspath(os.curdir)}/modules/games/templates/max_player_interaction.md', 'r') as f:
    PLAYER_MAX_INTERACTION_PROMPT = f.read()

class Game:
    player: str = None
    story: Story = None

    def __init__(self, player: str, story: Story):
        self.player = player
        self.story = story

    def start(self):
        print(f'Démmarage du jeu pour {self.player} !')
        story_plot = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": GENERATE_STORY_PROMPT},
                {"role": "user", "content": self.story.start}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=1.2,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.story.story_plot = story_plot.choices[0].message
        print(f'Story plot will be :\n{self.story.story_plot.content}')
        self.story.adventures.append({"role": "system", "content": GENERATE_ADVENTURE_PROMPT.format(
            story_plot=self.story.story_plot.content,
            max_player_interaction=self.story.max_player_interaction,
            player=self.player
        )})
        adventures = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.story.adventures,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.2,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.story.adventures.append(adventures.choices[0].message)
        print(f'First game message is :\n{self.story.adventures[-1].content}')
        return self.story.adventures[-1].content

    def end(self):
        pass

    def play(self, message):
        self.story.adventures.append({"role": "system", "content": PLAYER_MAX_INTERACTION_PROMPT.format(
            interactions_left=self.story.max_player_interaction -
            len(self.story.adventures)
        )})
        self.story.adventures.append({"role": "user", "content": message})
        adventures = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.story.adventures,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.2,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.story.adventures.append(adventures.choices[0].message)
        return adventures.choices[0].message.content
