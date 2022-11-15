class EmptyFileError(Exception):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __str__(self):
        return f'{self.file_name} is empty !'