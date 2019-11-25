class FileEntry:
    def __init__(self, name, length, cprsd_length, data=[]):
        self.name = name
        self.length = length
        self.cprsd_length = cprsd_length
        self.data = data
