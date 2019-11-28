HELP_TEXT = """
AWS S3 CLI Tool is used to get data of your s3 storage. Here are some of the available commands: \n

name           -- returns the names of the buckets. 
                Use the optional argument -f [filter string] to filter the bucket by name. \n 
size           -- returns the total size of each bucket in bytes. 
                Use the optional argument --kb --mb --gb to get the size in different units. \n
creationDate   -- returns the creation date of each bucket. \n
fileCount      -- returns the total number of files in each bucket.\n
lastModified   -- returns the name and time of the last modified object in each bucket. \n
region         -- returns each bucket grouped by their respective region. \n
storage        -- returns storage type of each object in the bucket. 
    """
HELP_CMD = 'The set of data to retrieve per bucket'
HELP_KB = 'when used the returned bucket size will be in kilobytes'
HELP_MB = 'when used the returned bucket size will be in megabytes'
HELP_GB = 'when used the returned bucket size will be in gigabytes'
HELP_F = 'when used it will return only buckets filtered with the string proceeding -f'
