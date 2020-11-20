from derpibooru import Search
import random
import utilities
import discord

def parametersValid(parameters):
    return parameters != ''

async def commands(message, path):
    await message.channel.send(
        """
        ```
I use natural language processing so you can talk to me with regular English!
I'll start listening when you start a message with "Hey Rarity", "Rarity", or "Okay Rarity"

For example: Hey Rarity, what commands do you understand?

However, if I'm having trouble understanding you, you can run specific commands by using the !rarity trigger.

For example: !rarity help

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

async def tellMeAJoke(message, path):
    jokes = [
        "You.",
        "What do you call it when your sister refuses to lower the moon?\nLunacy.",
        "Where do ponies go to get their shoes?\nFetlocker.",
        "What do you call a pretty rainbow pony?\nDashing.",
        "What do you call a Draconequus that is removed from MLP?\nDiscard.",
        "How many children does Celestia have?\nOne. The Sun.",
        "What's my favourite time of day?\nTwilight. mwa <3",
        "Darling, I'd love to tell you a joke, but my throat's feeling a little horse!",
        "Why is Winona not allowed to drive the tractor?\nShe received too many barking tickets.",
        "Why does Luna enjoy stopping ponies' nightmares?\nIt's her dream job.",
        "Why couldn't Applebloom charge her iPhone?\nShe needed an Applejack.",
        "I once bumped my head into a church bell.\nIt was the worst possible ding!",
        "Why doesn't Fluttershy use the elevator?\nShe's the stare master.",
        "Why did Twilight give her books to Rainbow?\nTo store it in the cloud.",
        "Why did Applejack lie?\nShe didn't. I lied.",
        "Where do ponies go when they're sick?\nThe horsepital.",
        "What do unicorns do during rush hour?\nThey honk their horns.",
        "A pony walks into a bar.\n Ouch.",
        "Why did Twilight's rune backfire?\nShe didn't run a spell check.",
        "Why did the CMCs cross the road?\nThe rest were just following Scootaloo.",
        "What car does Luna drive?\nA Moonborghini."
        ]
    await message.channel.send(random.choice(jokes))

async def emote(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name
    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT (source) FROM emotes WHERE name=%s;", (parameters[0], ))
        await message.channel.send(cursor.fetchone()[0])

async def emoteAdd(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name and [1] to be source
    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO emotes (name, source) VALUES (%s, %s);", (parameters[0], parameters[1]))
        connection.commit()
    await message.channel.send(f"Successfully added {parameters[0]} as an emote!")

async def emoteRemove(message, path):
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name
    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM emotes WHERE name=%s;", (parameters[0], ))
        connection.commit()
    await message.channel.send(f"Successfully removed {parameters[0]}.")

async def emoteList(message, path):
    connection = utilities.getDBConnection()
    output = "Emotes:\n"
    with connection.cursor() as cursor:
        cursor.execute("SELECT (name) FROM emotes;")
        for emote in cursor:
            output += f"{emote[0]}\n"
    await message.channel.send(output)

async def secretSantaInit(message: discord.Message, path):
    # State stuff
    state = utilities.getState()
    if state["secretSantaIsIniting"] == True:
        return
    state["secretSantaIsIniting"] = True
    utilities.setState(state)

    # Send initial message to server chat
    newMessage: discord.Message = await message.channel.send("Lets do a gift exchange! Respond to this message with :YES: to join in!")
    await newMessage.add_reaction("<:YES:774509192442150922>")

    # Listen for reactions in loop, send DM on reaction
    client = utilities.getDiscordClient()
    connection = utilities.getDBConnection()
    while utilities.getState()["secretSantaIsIniting"]:
        reaction, user = await client.wait_for('reaction_add', check= lambda reaction, user: str(reaction.emoji) == "<:YES:774509192442150922>" and user != newMessage.author)

        # Check if participant has already been added, skip if has
        with connection.cursor() as cursor:
            cursor.execute("SELECT (participant) FROM secret_santa WHERE participant=%s", (str(user.id), ))
            if cursor.fetchone() != None:
                continue

        # Add participant
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO secret_santa (season, participant) VALUES (%s, %s)", (1, user.id))
            connection.commit()

        await user.send("Run 'Rarity secret santa add prompt' to put your prompt into the system.")

async def secretSantaBegin(message, path):
    # Remove secret santa init reaction listener loop
    state = utilities.getState()
    state["secretSantaIsIniting"] = False
    utilities.setState(state)

# rarity secret santa add prompt I want you to draw a picture of my oc
async def secretSantaAddPrompt(message: discord.Message, path):
    userId = str(message.author.id)
    promptAttachments = list(map(lambda attachment: attachment.url, message.attachments))

    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
            cursor.execute("UPDATE secret_santa SET prompt=%s, prompt_attachments=%s WHERE participant=%s", (path, promptAttachments, userId))
            connection.commit()

async def secretSantaWithdraw(message, path):
    userId = str(message.author.id)

    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM secret_santa WHERE participant=%s;", (userId, ))
        connection.commit()

    await message.channel.send("You have successfully been removed from the secret santa event.")

async def naturalLanguageCommand(message, content):
    chatter = utilities.getChatter()
    arguments = [""]

    if isinstance(content, (tuple, list)):
        lowercaseContent, normalizedContent = content
        arguments = utilities.betweenQuotes(lowercaseContent)
    else:
        normalizedContent = content
        
    context, responseOrHandler = chatter.chat(normalizedContent)

    if isinstance(responseOrHandler, str):
        await message.channel.send(responseOrHandler)
    else:
        if arguments:
            await responseOrHandler(message, utilities.normalizeText(arguments[0]))
        else:
            await responseOrHandler(message, "")