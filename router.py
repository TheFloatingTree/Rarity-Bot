import discord

class Router:
    def __init__(self):
        self.commandMap = dict()

    def add(self, command):
        if command.message in self.commandMap:
            raise Exception("Command already exists")
        self.commandMap[command.message] = command

    async def resolve(self, message: discord.Message, path):
        if not path:
            return

        mostSpecificCommandMessage = ""
        for commandMessage in self.commandMap.keys():
            if path.startswith(commandMessage):
                mostSpecificCommandMessage = mostSpecificCommandMessage if len(mostSpecificCommandMessage) > len(commandMessage) else commandMessage

        if not mostSpecificCommandMessage:
            return
                
        commandArguments = path.replace(mostSpecificCommandMessage, '').strip()

        command = self.commandMap[mostSpecificCommandMessage]
        if not isinstance(message.channel, discord.DMChannel) and command.dmOnly:
            return

        await command.callback(message, commandArguments)