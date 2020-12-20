import openai
import discord
import json

from utilities import getState, setState
from appSettings import MAX_CONTEXT_SIZE

def getResponse(message: discord.Message):

    state = getState()

    username = message.author.display_name
    instructions = f"Rarity is a chatbot that acts like the character Rarity from the TV show My Little Pony: Friendship is Magic. You are a white unicorn with a purple mane and tail that is knowledgeable about fashion. You are talking with a person named {username}. "
    examples = "How are you?#I'm doing very well, darling!#"
    context = "".join(state["gpt-3_context"][username])
    query = f"{message.content}#"

    prompt = instructions + examples + context + query

    response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.6,
            max_tokens=64,
            top_p=1,
            stop=["#"]
            )
    responseBody = json.loads(response.last_response.body)
    responseContent = responseBody["choices"][0]["text"]

    # This sucks so bad, really need to refactor the getState and setState functions
    state["gpt-3_context"][username].append(f"{message.content}#{responseContent}#")
    state["gpt-3_context"][username] = state["gpt-3_context"][username][-MAX_CONTEXT_SIZE:]

    setState(state)

    return responseContent
    