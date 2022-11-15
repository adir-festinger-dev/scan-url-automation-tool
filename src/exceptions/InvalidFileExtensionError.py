class InvalidFileExtensionError(Exception):

    def __init__(self, file_extension: str):
        self.file_extension = file_extension

    def __str__(self):
        return f'The file extension of the file you entered is invalid !\nThe file extension of your file is {self.file_extension}.\nThe file extension should be .txt !'