from routes import *

data = [
    ("Help", commands),
    ("What can I say or ask you", commands),
    ("What commands can I give you", commands),

    ("Give or tell me a joke!", tellMeAJoke),

    ("Hello", hello),

    ("Show me a picture of a pony.", pony),
    ("Give me a random pony", pony),

    ("What do you think?", whatDoYouThink),
    ("Do you agree?", whatDoYouThink),
    ("Do you have an opinion?", whatDoYouThink),
    ("Are you sure about that?", whatDoYouThink),
    ("Can I have?", whatDoYouThink),

    ("Rate this out of ten 10", rateThis),
    ("Can you rate this?", rateThis),

    ("What emotes or emote do we have availible?", emoteList),
    ("What emotes are there?", emoteList),
    ("Give me the emote list", emoteList),

    ("Send an the emote", emote),

    ("Add an the emote", emoteAdd),

    ("Remove an the this emote", emoteRemove),

    ("Do you love twilight?", iLoveTwilight),

    ("emergency raritwi", emergencyRaritwi),
    ("I need some pictures of raritwi", emergencyRaritwi),
    ("I need raritwi", emergencyRaritwi),

    ("emergency rarity", emergencyRarity),
    ("I need some pictures of rarity", emergencyRarity),
    ("I need rarity", emergencyRarity),

    ("emergency twilight", emergencyTwilight),
    ("I need some pictures of twilight", emergencyTwilight),
    ("I need twilight", emergencyTwilight),

    ("Run this python code", runPython),
    ("Execute this python code", runPython),

    ("How are you?", "I'm doing very well, thank you!"),
    ("How are things?", "Things are going very well, thank you!"),
    ("Whats up?", "What's up!"),
    ("Are you best pony?", "Of course."),
]