class PathNotFileError(Exception):

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'The path: {self.path} is not a file !'