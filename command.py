class Command:
    def __init__(self, message, callback, helpText, dmOnly = False):
        self.message = message
        self.callback = callback
        self.helpText = helpText
        self.dmOnly = dmOnly