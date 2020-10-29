class Router:
    def __init__(self):
        self.tokenMap = dict()
        pass

    def add(self, tokens, _next):
        tokenList = tokens.split(' ')
        for token in tokenList[:-1]:
            self.tokenMap[token] = self.resolve
        self.tokenMap[tokenList[-1]] = _next

    async def resolve(self, message, path):
        if not path:
            return
        firstToken = path.partition(' ')[0] # get first token from path
        nextPath = path.partition(' ')[2] # remove first token from path, pass along
        await self.tokenMap[firstToken](message, nextPath)