import sys
import boto3
import botocore
from classmodule import MyClass
import s3funcmodule 
import argparse
import csv

def main():
    try:
        f = open('accessKeys.csv', 'r')
    except FileNotFoundError:
        sys.exit('Error: File does not exist. Please upload accessKeys.csv file into the root folder of s3cli')
    
    reader = csv.reader(f, delimiter=',')
    for col in reader:
          accessKey = col[0]
          secretKey = col[1]

    s3 = boto3.client('s3',
        aws_access_key_id=accessKey,
        aws_secret_access_key=secretKey
    )
    response = s3.list_buckets()
    
    parser = argparse.ArgumentParser(description='aws s3 cli')
    parser.add_argument('cmd', type=str, help='primary s3 command')
    parser.add_argument('--kb', action='store_true', help='when used with size the returned bucket size will be in kilobytes')
    parser.add_argument('--mb', action='store_true', help='when used with size the returned bucket size will be in megabytes')
    parser.add_argument('--gb', action='store_true', help='when used with size the returned bucket size will be in gigabytes')
    parser.add_argument('-f', type=str, help='use with filter command to return all buckets filtered with the string proceeding -f' )
    arg = parser.parse_args()

    if arg.cmd == 'name':
        s3funcmodule.getBucketName(response)
    if arg.cmd == 'creationDate':
        s3funcmodule.getBucketCreationDate(response)
    if arg.cmd == 'fileCount':
        s3funcmodule.getNumberOfObj(s3,response)
    if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3,response)
    if arg.cmd == 'size' and arg.kb == True and arg.mb == False and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3,response,'kb')
    if arg.cmd == 'size' and arg.kb == False and arg.mb == True and arg.gb == False:
        s3funcmodule.getTotalObjectSize(s3,response,'mb')
    if arg.cmd == 'size' and arg.kb == False and arg.mb == False and arg.gb == True:
        s3funcmodule.getTotalObjectSize(s3,response,'gb')
    if arg.cmd == 'lastModified':
        s3funcmodule.getLastModified(s3,response)
    if arg.cmd == 'region':
        s3funcmodule.getRegion(s3,response)
    if arg.cmd == 'storage':
        s3funcmodule.getStorageTypeOfObj(s3,response)
    if arg.cmd == 'filter':
        print(arg.f)
        s3funcmodule.getFilteredBucketName(s3, arg.f)

    if arg.cmd == '-res':
        for bucket in response['Buckets']:
            print(response)

if __name__ == '__main__':
    main()

