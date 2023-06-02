import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def send_message_to_discord(self, message):
        channel_id = 'your_discord_channel_id'  # Replace with your Discord channel ID
        channel = self.get_channel(int(channel_id))
        await channel.send(message)

discord_client = MyClient()
