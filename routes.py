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
To run a command use !rarity

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
    path = utilities.normalizeText(path)
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
        "What car does Luna drive?\nA Moonborghini.",
        "Neigh"
        ]
    await message.channel.send(random.choice(jokes))

async def emote(message, path):
    path = utilities.normalizeText(path)
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name
    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT (source) FROM emotes WHERE name=%s;", (parameters[0], ))
        await message.channel.send(cursor.fetchone()[0])

async def emoteAdd(message, path):
    path = utilities.normalizeText(path)
    if not parametersValid(path):
        return
    parameters = path.split(' ') # expects [0] to be name and [1] to be source
    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO emotes (name, source) VALUES (%s, %s);", (parameters[0], parameters[1]))
        connection.commit()
    await message.channel.send(f"Successfully added {parameters[0]} as an emote!")

async def emoteRemove(message, path):
    path = utilities.normalizeText(path)
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


# Move initing flag to persistant state
async def secretSantaInit(message: discord.Message, path):
    # State stuff
    state = utilities.getState()
    if state["secretSantaIsIniting"] == True:
        return
    state["secretSantaIsIniting"] = True
    utilities.setState(state)

    currentSeason = utilities.getPersistantState('secretSantaCurrentSeason')
    currentSeason = 1 if currentSeason == None else int(currentSeason) + 1
    utilities.setPersistantState('secretSantaCurrentSeason', currentSeason)

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
            cursor.execute("SELECT (participant) FROM secret_santa WHERE participant=%s AND season=%s", (str(user.id), currentSeason))
            if cursor.fetchone() != None:
                continue

        # Add participant
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO secret_santa (season, participant, gift_revealed) VALUES (%s, %s, %s)", (currentSeason, user.id, False))
            connection.commit()

        await user.send("Run '!rarity secret santa add prompt' to put your prompt into the system.")

async def secretSantaBegin(message, path):
    # Remove secret santa init reaction listener loop
    state = utilities.getState()
    state["secretSantaIsIniting"] = False
    utilities.setState(state)
    currentSeason = utilities.getPersistantState('secretSantaCurrentSeason')

    # Check to see if everyone has put in their prompts

    connection = utilities.getDBConnection()
    client = utilities.getDiscordClient()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM secret_santa WHERE prompt IS NULL AND season=%s", (currentSeason, ))

        allPromptsProvided = True
        response = "Some participants have not provided prompts:\n"
        for entry in cursor:
            allPromptsProvided = False
            user = await client.fetch_user(int(entry[2]))
            response += f"{user.name}\n"

        if not allPromptsProvided:
            await message.channel.send(response)
            return

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, participant, prompt, prompt_attachments FROM secret_santa WHERE season=%s", (currentSeason, ))
        participants = cursor.fetchall()

        # participants = list(map(tuple, participants))

        totalParticipants = len(participants)
        skip = random.randint(1, totalParticipants - 1)
        for participantIndex, participant in enumerate(participants):

            rowId, discordId, prompt, promptAttachments = participant
            discordUser = await client.fetch_user(int(discordId))

            # Pair participants in database

            partnerIndex = (participantIndex + skip) % totalParticipants

            partnerRowId, partnerDiscordId, partnerPrompt, partnerPromptAttachments = participants[partnerIndex]
            partnerDiscordUser = await client.fetch_user(int(partnerDiscordId))

            cursor.execute("UPDATE secret_santa SET paired_id=%s WHERE id=%s", (partnerRowId, rowId))
            connection.commit()

            # Send DM

            partnerUsername = partnerDiscordUser.name
            await discordUser.send(f'You are paired with {partnerUsername}.\nTheir prompt is:\n{partnerPrompt}\n{partnerPromptAttachments}')
            await discordUser.send("Run '!rarity secret santa add gift' to put your gift into the system.")

# TODO: Secret santa help command

async def secretSantaNext(message, path):
    currentSeason = utilities.getPersistantState('secretSantaCurrentSeason')

    connection = utilities.getDBConnection()
    client = utilities.getDiscordClient()
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM secret_santa WHERE gift IS NULL AND season=%s", (currentSeason, ))

        allGiftsProvided = True
        response = "Some participants have not provided gifts:\n"
        for entry in cursor:
            allGiftsProvided = False
            user = await client.fetch_user(int(entry[2]))
            response += f"{user.name}\n"

        if not allGiftsProvided:
            await message.channel.send(response)
            return

        cursor.execute("SELECT * FROM secret_santa WHERE season=%s AND gift_revealed=%s", (currentSeason, False))
        response = cursor.fetchone()
        if response == None:
            await message.channel.send("No more gifts to reveal!")
            return
        rowId, season, discordId, prompt, promptAttachment, pairedId, gift, giftRevealed = response

        cursor.execute("SELECT * FROM secret_santa WHERE id=%s", (pairedId, ))
        partnerRowId, partnerSeason, partnerDiscordId, partnerPrompt, partnerPromptAttachment, partnerPairedId, partnerGift, partnerGiftRevealed = cursor.fetchone()

        cursor.execute("UPDATE secret_santa SET gift_revealed=%s WHERE id=%s", (True, rowId))
        connection.commit()

        discordUser = await client.fetch_user(int(discordId))
        partnerDiscordUser = await client.fetch_user(int(partnerDiscordId))

        await message.channel.send(f'{discordUser.name} drew this for {partnerDiscordUser.name} based on the prompt "{partnerPrompt}"\n{gift}')

        # Person drew this for Partner based on the prompt "the prompt"
        # Gift

# TODO: command to display all gifts by season number

# rarity secret santa add prompt I want you to draw a picture of my oc
# Specify in instructions that this command takes one prompt and one image
async def secretSantaAddPrompt(message: discord.Message, path):
    userId = str(message.author.id)
    promptAttachments = list(map(lambda attachment: attachment.url, message.attachments))

    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        if promptAttachments:
            cursor.execute("UPDATE secret_santa SET prompt=%s, prompt_attachments=%s WHERE participant=%s", (path, promptAttachments[0], userId))
        else:
            cursor.execute("UPDATE secret_santa SET prompt=%s WHERE participant=%s", (path, userId))
        connection.commit()

    await message.channel.send("You have successfully added a prompt to the secret santa event.")

async def secretSantaAddGift(message: discord.Message, path):
    userId = str(message.author.id)
    promptAttachments = list(map(lambda attachment: attachment.url, message.attachments))

    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
            cursor.execute("UPDATE secret_santa SET gift=%s WHERE participant=%s", (promptAttachments[0], userId))
            connection.commit()

    await message.channel.send("You have successfully added your gift to the secret santa event.")

async def secretSantaWithdraw(message, path):
    userId = str(message.author.id)

    connection = utilities.getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM secret_santa WHERE participant=%s;", (userId, ))
        connection.commit()

    await message.channel.send("You have successfully been removed from the secret santa event.")

async def runPython(message, code):
    output = utilities.evaluatePython(code)
    await message.channel.send(output)