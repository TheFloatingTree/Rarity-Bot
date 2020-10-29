import discord
import os

from appSettings import isProduction
from router import Router
from routes import commands, hello, pony, iLoveTwilight, emergencyRaritwi, emergencyRarity, emergencyTwilight, test, whatDoYouThink

if not isProduction():
    import dotenv
    dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

client = discord.Client()
router = Router()

router.add('help', commands)
router.add('commands', commands)
router.add('hello', hello)
router.add('pony', pony)
router.add('i love twilight', iLoveTwilight)
router.add('emergency raritwi', emergencyRaritwi)
router.add('emergency rarity', emergencyRarity)
router.add('emergency twilight', emergencyTwilight)
# router.add('test', test)
# router.add('emote', hello)
# router.add('emote list', hello)
# router.add('emote add', hello)
# router.add('emote remove', hello)
router.add('what do you think', whatDoYouThink)
router.add('do you agree', whatDoYouThink)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Running in " + ("production" if isProduction() else "development") + " mode.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str.lower(message.content).startswith('rarity '):
        nextPath = str.lower(message.content).partition(' ')[2] # remove first token from path, pass along
        await router.resolve(message, nextPath)

client.run(BOT_TOKEN)
