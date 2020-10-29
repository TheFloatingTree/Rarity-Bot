from derpibooru import Search
import random
import dbConnect

def parametersValid(parameters):
    return parameters != ''

async def commands(message, path):
    await message.channel.send(
        """
        ```
To start talking to me, just preface any command with `rarity`
Commands:
    help                        Show help for commands.
    hello                       It's only fair to reciprocate!
    pony *tags                  Seach for pony images on derpibooru, tags are optional and separated by spaces.
    i love twilight             Send the gif.
    emergency raritwi           Raritwi pictures.
    emergency rarity            Rarity pictures.
    emergency twilight          Twilight pictures.

    what do you think           Decisions, decisions...
    rate this                   0/10 never using again.

    emote [name]                Do an emote.
    emote list                  List all availible emotes.
    emote add [name] [source]   Add a new emote.
    emote remove [name]         Remove an old emote.```
        """
        )

async def hello(message, path):
    await message.channel.send("Hello!")

async def pony(message, path):
    tags = path.split(' ')
    for image in Search().query("safe", *tags).sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def iLoveTwilight(message, path):
    await message.channel.send('https://media.discordapp.net/attachments/392164092959260674/752326934691577966/RariTwiKissu.gif')

async def emergencyRaritwi(message, path):
    for image in Search().query("rarilight", "pony", "safe").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def emergencyRarity(message, path):
    for image in Search().query("rarity", "pony", "safe", "solo").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def emergencyTwilight(message, path):
    for image in Search().query("ts", "pony", "safe", "solo").sort_by("random").limit(1):
        await message.channel.send(image.medium)

async def whatDoYouThink(message, path):
    if bool(random.getrandbits(1)):
        await message.channel.send("Hmm, yes, I agree.")
    else:
        await message.channel.send("Hmm, no, I don't agree.")

async def rateThis(message, path):
    rating = random.randint(0, 10)
    await message.channel.send(f"I give it {rating}/10")

async def emote(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name
    connection = dbConnect.getConnection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT (source) FROM emotes WHERE name=%s;", (parameters[0], ))
        await message.channel.send(cursor.fetchone()[0])

async def emoteAdd(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name and [1] to be source
    connection = dbConnect.getConnection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO emotes (name, source) VALUES (%s, %s);", (parameters[0], parameters[1]))
        connection.commit()
    await message.channel.send(f"Successfully added {parameters[0]} as an emote!")

async def emoteRemove(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name
    connection = dbConnect.getConnection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM emotes WHERE name=%s;", (parameters[0], ))
        connection.commit()
    await message.channel.send(f"Successfully removed {parameters[0]}.")

async def emoteList(message, path):
    connection = dbConnect.getConnection()
    output = "Emotes:\n"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM emotes;")
        for emote in cursor:
            output += f"{emote[1]}\n"
    await message.channel.send(output)