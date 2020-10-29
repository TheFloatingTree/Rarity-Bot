import discord
import os

from router import Router
from routes import commands, hello, pony, emergencyRaritwi, emergencyRarity, emergencyTwilight

token = "NzcxMjQzNDQ4OTI5MjIyNjc3.X5pSbw.Zxezhmt5sNxbNaOwSrpWaynbOkc"
client = discord.Client()
router = Router()

router.add('help', commands)
router.add('commands', commands)
router.add('hello', hello)
router.add('pony', pony)
router.add('emergency raritwi', emergencyRaritwi)
router.add('emergency rarity', emergencyRarity)
router.add('emergency twilight', emergencyTwilight)

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