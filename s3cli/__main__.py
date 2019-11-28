import sys
import boto3
import botocore
import bucketWorker
import argparse
import Bucket
import csv
from argparse import RawTextHelpFormatter
import constants


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
    s3Cost = boto3.client('ce',
                          aws_access_key_id=accessKey,
                          aws_secret_access_key=secretKey
                          )
    parser = argparse.ArgumentParser(
        description=constants.HELP_TEXT, formatter_class=RawTextHelpFormatter)
    parser.add_argument('cmd', type=str,
                        help=constants.HELP_CMD, nargs='*')
    parser.add_argument('--kb', action='store_true',
                        help=constants.HELP_KB)
    parser.add_argument('--mb', action='store_true',
                        help=constants.HELP_MB)
    parser.add_argument('--gb', action='store_true',
                        help=constants.HELP_GB)
    parser.add_argument(
        '-f', type=str, help=constants.HELP_F)

    arg = parser.parse_args()
    param = GetParams(arg)
    bucketWorker.ProcessBucket(response, s3Client, s3Resource, param)
    # print(arg)
    # if arg.cmd == 'name':
    #     if arg.f is not None:
    #         bucketWorker.getFilteredBucketName(s3Resource, arg.f)
    #     else:
    #         bucketWorker.getBucketName(response)
    # if arg.cmd == 'cd':
    #     bucketWorker.getBucketCreationDate(response)
    # if arg.cmd == 'fc':
    #     bucketWorker.getNumberOfObj(s3Client, response)
    # if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == False:
    #     bucketWorker.getTotalObjectSize(s3Resource, response)
    # if arg.cmd == 'size' and arg.kb == True and arg.mb == False and arg.gb == False:
    #     bucketWorker.getTotalObjectSize(s3Resource, response, 'kb')
    # if arg.cmd == 'size' and arg.kb == False and arg.mb == True and arg.gb == False:
    #     bucketWorker.getTotalObjectSize(s3Resource, response, 'mb')
    # if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == True:
    #     bucketWorker.getTotalObjectSize(s3Resource, response, 'gb')
    # if arg.cmd == 'lm':
    #     bucketWorker.getLastModified(s3Client, response)
    # if arg.cmd == 'region':
    #     bucketWorker.getRegion(s3Client, response)
    # if arg.cmd == 'storage':
    #     bucketWorker.getStorageTypeOfObj(s3Client, response)
    # if arg.cmd == 'cost':
    #     bucketWorker.getCost()


# processing methods
def GetParams(arg):
    return {
        'size': 'size' in arg.cmd,
        'fileCount': 'fileCount' in arg.cmd,
        'creationDate': 'creationDate' in arg.cmd,
        'lastModified': 'lastModified' in arg.cmd,
        'storage': 'storage' in arg.cmd,
        'region': 'region' in arg.cmd,
        'cost': 'cost' in arg.cmd,
        'size_kb': arg.kb,
        'size_mb': arg.mb,
        'size_gb': arg.gb,
        'f': arg.f
    }


def PrintResult(result):
    # print by region, then top level bucket info, then object list
    print("fucku")


if __name__ == '__main__':
    main()
