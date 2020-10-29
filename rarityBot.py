import discord
import requests
from derpibooru import Search, sort
import os

token = os.environ.get('token')
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send('Commands:\n$hello\n$pony\n$ilovetwilight\n$emergencyraritwi\n$rarity')

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$pony'):
        response = requests.get('https://theponyapi.com/api/v1/pony/random')
        data = response.json()
        await message.channel.send(data['pony']['representations']['medium'])

    if message.content.startswith('$ilovetwilight'):
        await message.channel.send('https://media.discordapp.net/attachments/392164092959260674/752326934691577966/RariTwiKissu.gif')

    if message.content.startswith('$emergencyraritwi'):
        for image in Search().query("rarilight", "pony", "safe").sort_by("random").limit(1):
            await message.channel.send(image.medium)

    if message.content.startswith('$rarity'):
        for image in Search().query("rarity", "pony", "safe", "solo").sort_by("random").limit(1):
            await message.channel.send(image.medium)

client.run(token)