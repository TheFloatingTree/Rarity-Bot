import discord
import os

from router import Router
from routes import commands, hello, pony, emergencyRaritwi, emergencyRarity, emergencyTwilight, whatDoYouThink

token = os.environ.get('token')
client = discord.Client()
router = Router()

router.add('help', commands)
router.add('commands', commands)
router.add('hello', hello)
router.add('pony', pony)
router.add('emergency raritwi', emergencyRaritwi)
router.add('emergency rarity', emergencyRarity)
router.add('emergency twilight', emergencyTwilight)
router.add('what do you think', whatDoYouThink)
router.add('do you agree', whatDoYouThink)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str.lower(message.content).startswith('rarity '):
        nextPath = str.lower(message.content).partition(' ')[2] # remove first token from path, pass along
        await router.resolve(message, nextPath)

client.run(token)