import sys
import boto3
import botocore
import BucketWorker
import argparse
import Bucket
import csv
from argparse import RawTextHelpFormatter
import constants
import os.path

def main():
   # try to open and retrieve access and secret keys from csv file
    try:
        f = open('accessKeys.csv', 'r')
        reader = csv.reader(f, delimiter=',')
        for col in reader:
            accessKey = col[0]
            secretKey = col[1]
        # connect to s3 client and resourse using the keys retrieved
        s3Client = boto3.client('s3',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
        s3Resource = boto3.resource('s3',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
        s3Cost = boto3.client('ce',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
        response = s3Client.list_buckets()
    except FileNotFoundError:
        print('Error: accessKeys.csv does not exist. Please follow along below or upload accessKeys.csv file into the root folder of s3cli')
        
        check = input("Does your machine have aws cli installed and configured? Enter (y/n): ")
        if(check == 'n'):
            accessKey = input("Please enter your access key: ")
            secretKey = input("Please enter your secret key: ")
            s3Client = boto3.client('s3',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
            s3Resource = boto3.resource('s3',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
            s3Cost = boto3.client('ce',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey
                    )
            response = s3Client.list_buckets()
        else:
            print('Connecting to s3 using using the keys from your ~/.aws/credentials')
            s3Client = boto3.client('s3')
            s3Resource = boto3.resource('s3')
            s3Cost = boto3.client('ce')
            response = s3Client.list_buckets()
       
    # argument parser
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
    result = BucketWorker.ProcessBucket(response, s3Client, s3Resource, param)
    PrintResult(result, arg)

# checks which cmd are called in the argument and sets it accordingly if it exists


def GetParams(arg):
    return {
        'objectParams': {
            'size': 'size' in arg.cmd,
            'fileCount': 'fileCount' in arg.cmd,
            'storage': 'storage' in arg.cmd,
            'lastModified': 'lastModified' in arg.cmd
        },
        'creationDate': 'creationDate' in arg.cmd,
        'cost': 'cost' in arg.cmd,
        'size_kb': arg.kb,
        'size_mb': arg.mb,
        'size_gb': arg.gb,
        'f': arg.f
    }

# uses response results to print out the data requested from the command line arguments


def PrintResult(result, arg):
    for region in result.keys():
        print("Listing all buckets in: {}".format(region))
        for bucket in result[region]:
            print(bucket.name)
            if 'size' in arg.cmd and arg.kb == False and arg.mb == False and arg.gb == False:
                print('|__ Size: {} bytes'.format(bucket.size_bytes))
            if 'size' in arg.cmd and arg.kb == True:
                print('|__ Size: {} kb'.format(bucket.size_kb()))
            if 'size' in arg.cmd and arg.mb == True:
                print('|__ Size: {} mb'.format(bucket.size_mb()))
            if 'size' in arg.cmd and arg.gb == True:
                print('|__ Size: {} gb'.format(bucket.size_gb()))
            if 'fileCount' in arg.cmd:
                print('|__ File Count: {}'.format(bucket.fileCount))
            if 'creationDate' in arg.cmd:
                print('|__ Creation Date: {}'.format(bucket.creationDate))
            if 'lastModified' in arg.cmd:
                print('|__ Last Modified: {} -- Modified at: {}'.format(
                    bucket.lastModifiedFile, bucket.lastModifiedDate))
            if 'storage' in arg.cmd:
                for k, v in bucket.storage.items():
                    print('|__ File: {}: {}'.format(k, v))
                

        # print(b.cost)


if __name__ == '__main__':
    main()
