class Router:
    def __init__(self):
        self.commandMap = dict()

    def add(self, command, callback):
        if command in self.commandMap:
            raise Exception("Command already exists")
        self.commandMap[command] = callback

    async def resolve(self, message, path):
        if not path:
            return

        mostSpecificCommand = ""
        for command in self.commandMap.keys():
            if path.startswith(command):
                mostSpecificCommand = mostSpecificCommand if len(mostSpecificCommand) > len(command) else command

        if not mostSpecificCommand:
            return
                
        commandArguments = path.replace(mostSpecificCommand, '').strip()
        await self.commandMap[mostSpecificCommand](message, commandArguments)