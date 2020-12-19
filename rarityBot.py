import discord
import os
import re
import openai
import json

from appSettings import isProduction
from router import Router
from routes import *
from utilities import getDiscordClient, startsWithAny, replaceAnyFront, cleanUpDBConnection
from command import Command


if not isProduction():
    import dotenv
    dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = getDiscordClient()
router = Router()

router.add(Command('help', commands, "Show help for commands."))
router.add(Command('hello', hello, "It's only fair to reciprocate!"))

router.add(Command('pony', pony, ""))

router.add(Command('i love twilight', iLoveTwilight, ""))

router.add(Command('emergency raritwi', emergencyRaritwi, ""))
router.add(Command('emergency rarity', emergencyRarity, ""))
router.add(Command('emergency twilight', emergencyTwilight, ""))

router.add(Command('what do you think', whatDoYouThink, ""))
router.add(Command('do you agree', whatDoYouThink, ""))
router.add(Command('rate this', rateThis, ""))
router.add(Command('tell me a joke', tellMeAJoke, ""))
router.add(Command('tell me another joke', tellMeAJoke, ""))

router.add(Command('emote', emote, ""))
router.add(Command('emote list', emoteList, ""))
router.add(Command('emote add', emoteAdd, ""))
router.add(Command('emote remove', emoteRemove, ""))

router.add(Command('secret santa init', secretSantaInit, ""))
router.add(Command('secret santa begin', secretSantaBegin, ""))
router.add(Command('secret santa add prompt', secretSantaAddPrompt, "", dmOnly=True))
router.add(Command('secret santa withdraw', secretSantaWithdraw, "", dmOnly=True))
router.add(Command('secret santa add gift', secretSantaAddGift, "", dmOnly=True))
router.add(Command('secret santa next', secretSantaNext, ""))

router.add(Command('natural language command', naturalLanguageCommand, ""))
router.add(Command('run', runPython, ""))

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Running in " + ("production" if isProduction() else "development") + " mode.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    triggerWords = ["rarity", "hey rarity", "ok rarity", "okay rarity", "so rarity", "yo rarity", "sup rarity"]

    lowercaseContent = str(message.content).lower()
    normalizedContent = re.sub(r'[^ a-z]', '', lowercaseContent)

    if lowercaseContent.startswith('!rarity'):
        nextPath = str.lower(message.content).partition(' ')[2] # remove first token from path, pass along
        await router.resolve(message, nextPath)
    elif startsWithAny(normalizedContent, triggerWords):
        response = openai.Completion.create(
            engine="davinci",
            prompt="Rarity is a chatbot that acts like the character Rarity from the TV show My Little Pony: Friendship is Magic. She is an elegant white unicorn with a purple mane that likes to make dresses.#How are you?#I'm doing very well, darling!#" + message.content + "#",
            temperature=0.6,
            max_tokens=64,
            top_p=1,
            stop=["#"]
            )
        responseBody = json.loads(response.last_response.body)
        text = responseBody["choices"][0]["text"]
        await message.channel.send(text)

        
        
client.run(BOT_TOKEN)

cleanUpDBConnection()