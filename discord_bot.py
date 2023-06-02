import discord

import asyncio

class DiscordBot(discord.Client):
    token: str = None
    channel_id: int = None

    def __init__(self, token: str, channel: int):
        self.token = token
        self.channel_id = channel
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        print('Logged to Discord as', self.user)

    async def send_message_to_discord(self, message):
        channel = self.get_channel(self.channel_id)
        await channel.send(message)
