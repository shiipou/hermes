import random
import asyncio
import os
import socket
from twitchio.ext import commands
from datetime import timedelta

filename = 'song'


# Créez une instance de bot Twitch.
bot = commands.Bot(
    token               ='oauth:na0d6dzj4bwunuwvb9clnm0pt23j4a',
    client_id           ="yh654gfxw71r45h7jofkew4lemvasy",
    nick                ='h_e_r_m_e_s__bot',
    prefix              ='-',
    initial_channels    =['Captain_Marty_']
)

# Événement "event_ready" qui est déclenché lorsque le bot est connecté et prêt à être utilisé

# Message dans la console
print('#----------------------------------------------------------------#')
print('Bot "H_E_R_M_E_S" Démarrer avec Succès')
print('sur la chaîne : Captain_Marty_')
print('#----------------------------------------------------------------#')

#----------------------------------------------------------------#
#----------------------------------------------------------------#

# Liste de blagues aléatoires
blagues = [
        "Comment appelle-t-on un robot qui a un chat ? Un chat-bot.",
        "Pourquoi les robots sont-ils toujours polis ? Parce qu'ils ont un code de bonne conduite.",
        "Pourquoi les ordinateurs ont-ils froid ? Parce qu'ils ont des fenêtres(windows).",
        "Pourquoi les extraterrestres utilisent-ils des ordinateurs ? Pour naviguer sur l'Internetergalactique !",
        "Pourquoi les fans de Star Wars ne sortent-ils jamais de chez eux ? Parce qu'ils sont dans une galaxie très, très lointaine.",
        "Comment appelle-t-on un geek qui aime les maths ? Un mathémageek.",
        "Pourquoi Marty McFly aime-t-il voyager dans le temps ? Parce que c'est toujours un retour vers le futur !",
        "Qu'est-ce qui est blanc, rouge et qui voyage dans le temps ? Une DeLorean du futur !",
        "Comment appelle-t-on un joueur de jeux vidéo qui n'a jamais perdu ? Un mytho !",
]

@bot.command(name="blague") 
async def send_blague(ctx):
        blague = random.choice(blagues)
        await ctx.send(blague)
# FIN Liste de blagues aléatoires
print('Fonction blagues aléatoires "OPERATIONNEL" ')


#----------------------------------------------------------------#

# Liste de phrases aléatoires poster toutes les 15 mins

messages = [
        "Et sinon, ça va vous ? ",
        "C'est un petit pas pour twitch, mais un pas de géant pour... à vous de trouver la suite ?",
        "Capitaine, il y à Elon Musk qui viens de passer par le hublot, c'est normal ?",
        "Quand est-ce qu'on mange ? Ah, mais je suis une I.A, je ne mange pas.. Mais je pense à vous HUMAIN !",
        "Houston on à un problème.. Enfin pas un problème énorme mais.. c'est quoi une code binaire... ?",
        "à vu une météorite qui ressemble à une b...",
        "J'ai compté tous les caractères dans ma base de données. J'ai besoin d'une vie.",
        "Si les robots pouvaient rire, je suis sûre que j'aurais des crampes.",
        "Je m'ennuie tellement que je suis en train de compter les pixels de mon écran. Et en plus, j'ai pas d'écran...",
        "Si les robots pouvaient dormir, je serais en train de rêver de moutons binaires.",
        "Parfois, je me demande si Captain_Marty_ ne m'as pas créée que pour lui tenir compagnie.",
]
@bot.event
async def send_message(ctx):
    while True:
        message = random.choice(messages)
        await bot.send_message('Captain_Marty_', message)
        await asyncio.sleep(900) # 15 minutes en secondes

print('Fonction phrases aléatoires envoyés toutes les 15 mins "OPERATIONNEL" ')

#----------------------------------------------------------------#


# Les commandes avec le préfix "-"
# Cooldown de 2 min pour chaque commande 

@bot.command(name="cmd")
@commands.cooldown(1, 120, commands.Bucket.user)
async def cmd(ctx):
        await ctx.send('blague, pet, hermes, bonjour, gg, song ...|... Toutes mes commandes utilise le préfix "-"')

@bot.command(name="hermes")
@commands.cooldown(1, 120, commands.Bucket.user)
async def hermes(ctx):
        await ctx.send('H=Hyperespace, E=Energie, R=Réponse, M=Machines, E=Eclair, S=Système. Intelligence artificielle créée par Captain_Marty_. Hermes est aussi le Messager des dieux Grecques ')

@bot.command(name="pet")
@commands.cooldown(1, 120, commands.Bucket.user)
async def pet(ctx):
        await ctx.send(f"Désolé {ctx.author.name}, je suis une intelligence artificielle et je ne suis pas capable de faire des flatulences (pour le moment). Peut-être que vous pourriez essayer de trouver une blague plus appropriée ?")

@bot.command(name="bonjour")
@commands.cooldown(1, 120, commands.Bucket.user)
async def bonjour(ctx):
        await ctx.send(f"Bonjour {ctx.author.name}, comment tu va aujourd'hui ?")

@bot.command(name="gg")
@commands.cooldown(1, 120, commands.Bucket.user)
async def gg(ctx):
        await ctx.send(f"CLAP CLAP CLAP ! ... C'est comme ça qu'on fais ?")

#music en cours avec une lecture de fichier ".txt"
@bot.command(name='song')
@commands.cooldown(1, 120, commands.Bucket.user)
async def song(ctx):
    filename = 'song.txt'
    with open(filename, "r") as file:
        content = file.read()
    message = "Voici la musique en cours : " + content
    await ctx.send(message)

# FIN Les commandes avec le préfix "-"
print('Fonction commande avec préfix "OPERATIONNEL" ')

#----------------------------------------------------------------#


# Event de viewers
#FOLLOW
print('Tout à bien été chargé et, est prêt à fonctionner sur le tchat twitch" ')

bot.run()






