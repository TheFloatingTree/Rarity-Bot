from derpibooru import Search
import random

async def commands(message, path):
    await message.channel.send(
        """
        To start talking to me, just preface any command with `rarity`
        Commands:
            help                Show help for commands.
            hello               It's only fair to reciprocate!
            pony *tags          Seach for pony images on derpibooru, tags are optional and separated by spaces.
            i love twilight     Send the gif.
            emergency raritwi   Raritwi pictures.
            emergency rarity    Rarity pictures.
            emergency twilight  Twilight pictures.
            what do you think   Decisions, decisions...
        """
        )

async def hello(message, path):
    await message.channel.send("Hello!")

async def pony(message, path):
    tags = path.split(' ')
    for image in Search().query("pony", "safe", "solo", *tags).sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def iLoveTwilight(message, path):
    await message.channel.send('https://media.discordapp.net/attachments/392164092959260674/752326934691577966/RariTwiKissu.gif')

async def emergencyRaritwi(message, path):
    for image in Search().query("rarilight", "pony", "safe").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def emergencyRarity(message, path):
    for image in Search().query("rarity", "pony", "safe").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def emergencyTwilight(message, path):
    for image in Search().query("twilight", "pony", "safe").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def whatDoYouThink(message, path):
    if bool(random.getrandbits(1)):
        await message.channel.send("Hmm, yes, I agree.")
    else:
        await message.channel.send("Hmm, no, I don't agree.")