class Bucket(object):

    def __init__(self):
        self.name = ''
        self.size_bytes = 0
        self.fileCount = 0
        self.creationDate = ''
        self.lastModifiedDate = ''
        self.lastModifiedFile = ''
        self.storage = {}
        self.region = ''
        self.cost = ''

    def size_kb(self):
        return self.size_bytes/1000

    def size_mb(self):
        return self.size_bytes/1000000

    def size_gb(self):
        return self.size_bytes/1000000000
