import sys
import boto3
import botocore
import s3funcmodule
import argparse
import csv
from argparse import RawTextHelpFormatter


def main():
   # try to open and retrieve access and secret keys from csv file
    try:
        f = open('accessKeys.csv', 'r')
    except FileNotFoundError:
        sys.exit(
            'Error: File does not exist. Please upload accessKeys.csv file into the root folder of s3cli')

    reader = csv.reader(f, delimiter=',')
    for col in reader:
        accessKey = col[0]
        secretKey = col[1]

    # connect to s3 client and resourse using the keys retrieved
    s3Client = boto3.client('s3',
                            aws_access_key_id=accessKey,
                            aws_secret_access_key=secretKey
                            )
    response = s3Client.list_buckets()
    s3Resource = boto3.resource('s3',
                                aws_access_key_id=accessKey,
                                aws_secret_access_key=secretKey
                                )
    parser = argparse.ArgumentParser(description="""
AWS S3 CLI Tool is used to get data of your s3 storage. Here are some of the available commands: \n

   name -- returns the names of the buckets. 
           Use the optional argument -f [filter string] to filter the bucket by name. \n 
   size -- returns the total size of each bucket in bytes. 
           Use the optional argument --kb --mb --gb to get the size in different units. \n
    cd  -- returns the creation date of each bucket. \n
    fc  -- returns the total number of files in each bucket.\n
    lm  -- returns the name and time of the last modified object in each bucket. \n
region  -- returns each bucket grouped by their respective region. \n
storage -- returns storage type of each object in each bucket. 
    """, formatter_class=RawTextHelpFormatter)
    parser.add_argument('cmd', type=str,
                        help='pos arg')
    parser.add_argument('--kb', action='store_true',
                        help='when used with size the returned bucket size will be in kilobytes')
    parser.add_argument('--mb', action='store_true',
                        help='when used with size the returned bucket size will be in megabytes')
    parser.add_argument('--gb', action='store_true',
                        help='when used with size the returned bucket size will be in gigabytes')
    parser.add_argument(
        '-f', type=str, help='use with name command to return all buckets filtered with the string proceeding -f')
    arg = parser.parse_args()

    if arg.cmd == 'name':
        if arg.f is not None:
            s3funcmodule.getFilteredBucketName(s3Resource, arg.f)
        else:
            s3funcmodule.getBucketName(response)
    if arg.cmd == 'cd':
        s3funcmodule.getBucketCreationDate(response)
    if arg.cmd == 'fc':
        s3funcmodule.getNumberOfObj(s3Client, response)
    if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3Resource, response)
    if arg.cmd == 'size' and arg.kb == True and arg.mb == False and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3Resource, response, 'kb')
    if arg.cmd == 'size' and arg.kb == False and arg.mb == True and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3Resource, response, 'mb')
    if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == True:
        s3funcmodule.getTotalObjectSize(s3Resource, response, 'gb')
    if arg.cmd == 'lm':
        s3funcmodule.getLastModified(s3Client, response)
    if arg.cmd == 'region':
        s3funcmodule.getRegion(s3Client, response)
    if arg.cmd == 'storage':
        s3funcmodule.getStorageTypeOfObj(s3Client, response)


if __name__ == '__main__':
    main()
