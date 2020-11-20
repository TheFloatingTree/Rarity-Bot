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

    ("Rate this out of ten 10", rateThis),

    ("What emotes or emote do we have availible?", emoteList),
    ("What emotes are there?", emoteList),
    ("Give me the emote list", emoteList),

    ("Send an the emote", emote),
    ("Add an the emote", emoteAdd),
    ("Remove an the emote", emoteRemove),

    ("Do you love twilight?", iLoveTwilight),

    ("emergency raritwi", emergencyRaritwi),

    ("emergency rarity", emergencyRarity),

    ("emergency twilight", emergencyTwilight),

    ("How are you?", "I'm doing very well, thank you!"),
    ("How are things?", "Things are going very well, thank you!"),
    ("Whats up?", "What's up!"),
]