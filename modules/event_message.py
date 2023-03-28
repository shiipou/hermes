import random
import asyncio

wakeup_message = 'Je viens de me réveiller! Je suis prêt à vous divertir pour le stream !'


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