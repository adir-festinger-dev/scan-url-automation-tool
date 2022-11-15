class InvalidURLError(Exception):

    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def __str__(self):
        return f'URL syntax invalid in line {self.line}.\n{self.message}'