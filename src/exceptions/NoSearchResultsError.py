class NoSearchResultsError(Exception):

    def __init__(self, line: int):
        self.line = line

    def __str__(self):
        return f'There are no search results for url in line {self.line}.'