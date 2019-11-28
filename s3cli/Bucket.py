class Bucket:
    name = ''
    size_bytes = 0
    fileCount = 0
    creationDate = ''
    lastModified = ''
    storage = {'Key': '', 'StorageClass': ''}
    region = ''
    cost = ''
    f = ''

    def size_kb(self):
        return size_bytes/1000

    def size_mb(self):
        return size_byte/1000000

    def size_gb(self):
        return size_byte/1000000000
