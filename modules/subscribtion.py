import twitchio
import random

class SubscriptionCog(twitchio.ext.commands.Cog):
    def __init__(self, bot: twitchio.ext.commands.Bot):
        self.bot = bot
        
    @twitchio.ext.commands.Cog.event()
    async def on_subscription(self, subscription):
        follow_random = ["Bienvenue à bord de la station !",
                         "Installe-toi confortablement dans la station  !",
                         "Profite bien du stream interstellaire !",
                         "N'hésite pas à participer au live !"]
        user = subscription.user_name
        channel = subscription.channel_name
        message = random.choice(follow_random)
        await self.bot.send_message(channel, f"captai1440Heyfree Merci {user} d'avoir suivi la chaîne ! {message} captai1440Heyfree")
