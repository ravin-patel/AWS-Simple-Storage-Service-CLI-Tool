import boto3
import sys
import botocore
from datetime import datetime, timedelta

# iterates through all buckets returned in the response and prints the creation date of each bucket


def getBucketCreationDate(response):
    for bucket in response['Buckets']:
        print('Creation date of {} : {}'.format(
            bucket['Name'], bucket['CreationDate'].ctime()))

# iterates through all buckets returned in the response and prints the name of each bucket


def getCost():

    # use the bota3 lib to get the cost/usage
    # res = client.get_cost_and_usage(TimePeriod={
    #     'Start': '2019-11-01',
    #     'End': '2019-11-27'
    # })
    test_res = {
        "GroupDefinitions": [
            {
                "Key": "SERVICE",
                "Type": "DIMENSION"
            },
            {
                "Key": "Environment",
                "Type": "TAG"
            }
        ],
        "ResultsByTime": [
            {
                "Estimated": False,
                "Groups": [
                    {
                        "Keys": [
                            "AWS BUCKET 1",
                            "Environment$Prod"
                        ],
                        "Metrics": {
                            "BlendedCost": {
                                "Amount": "39.1603300457",
                                "Unit": "USD"
                            },
                            "UnblendedCost": {
                                "Amount": "39.1603300457",
                                "Unit": "USD"
                            },
                            "UsageQuantity": {
                                "Amount": "173842.5440074444",
                                "Unit": "N/A"
                            }
                        }
                    },
                    {
                        "Keys": [
                            "AWS BUCKET 2",
                            "Environment$Test"
                        ],
                        "Metrics": {
                            "BlendedCost": {
                                "Amount": "0.1337464807",
                                "Unit": "USD"
                            },
                            "UnblendedCost": {
                                "Amount": "0.1337464807",
                                "Unit": "USD"
                            },
                            "UsageQuantity": {
                                "Amount": "15992.0786663399",
                                "Unit": "N/A"
                            }
                        }
                    }
                ],
                "TimePeriod": {
                    "End": "2017-10-01",
                    "Start": "2017-09-01"
                },
                "Total": {}
            }
        ]
    }

    buckets = dict()
    for x in test_res["ResultsByTime"][0]["Groups"]:
        metrics = x["Metrics"]
        buckets[x["Keys"][0]] = float(metrics["BlendedCost"]["Amount"]) + float(
            metrics["UnblendedCost"]["Amount"]) + float(metrics["UsageQuantity"]["Amount"])
    print(buckets)


def getBucketName(response):
    for bucket in response['Buckets']:
        print('Name of bucket: {}'.format(bucket['Name']))

# iterates through passed in bucket and returns the name of each key(object) in that bucket


def listBucketObj(s3, bucket):
    paginator = s3.get_paginator("list_objects")
    for bucket in response['Buckets']:
        page_iterator = paginator.paginate(Bucket=bucket['Name'])
        for page in page_iterator:
            if "Contents" in page:
                for key in page["Contents"]:
                    print(
                        'Name of bucket: {} -- Name of Key: {}'.format(bucket['Name'], key["Key"]))


def getStorageTypeOfObj(s3, response):
    paginator = s3.get_paginator("list_objects")
    for bucket in response['Buckets']:
        page_iterator = paginator.paginate(Bucket=bucket['Name'])
        for page in page_iterator:
            # print(page['Contents'])
            if 'Contents' in page:
                for key in page['Contents']:
                    print(
                        'Name of Key: {} -- StorageClass: {}'.format(key['Key'], key['StorageClass']))
            else:
                print("cant get")


def getLastModified(s3, response):
    paginator = s3.get_paginator("list_objects")
    for bucket in response['Buckets']:
        bucketName = bucket['Name']
        page_iterator = paginator.paginate(Bucket=bucketName)
        format = '%Y-%m-%d %H:%M:%S+00:00'
        lastModifiedDate = datetime(1900, 1, 1, 0)
        lastModifiedObj = ""
        for page in page_iterator:
            if "Contents" in page:
                for key in page["Contents"]:
                    dt = key['LastModified']
                    if(datetime.strptime(str(dt), format) > lastModifiedDate):
                        lastModifiedDate = datetime.strptime(str(dt), format)
                        lastModifiedObj = key['Key']
        print(bucketName)
        print('Last modified file: {} -- modified on: {} \n'.format(lastModifiedObj, lastModifiedDate))

# iterates through all buckets returned in the response and prints the number of keys/objects in each bucket


def getNumberOfObj(s3, response):
    paginator = s3.get_paginator("list_objects")
    for bucket in response['Buckets']:
        count = 0
        page_iterator = paginator.paginate(Bucket=bucket['Name'])
        for page in page_iterator:
            if "Contents" in page:
                for key in page["Contents"]:
                    count += 1
        print('Number of files in {}: {}'.format(bucket['Name'], count))

# iterates through all buckets and returns the total size in either bytes/kb/mb


def getTotalObjectSize(s3, response, unit='bytes'):
    for bucket in response['Buckets']:
        totalSize = sum(
            [object.size for object in s3.Bucket(bucket['Name']).objects.all()])
        if str(unit) == 'kb':
            print('Total size of {}: {} kb'.format(
                bucket['Name'], totalSize/1000))
        elif unit == 'mb':
            print('Total size of {}: {} mb'.format(
                bucket['Name'], totalSize/1000000))
        elif unit == 'gb':
            print('Total size of {}: {} GB'.format(
                bucket['Name'], totalSize/1000000000))
        else:
            print('Total size of {}: {} bytes'.format(
                bucket['Name'], totalSize))


def getFilteredBucketName(s3, prefix):
    for bucket in s3.buckets.all():
        if bucket.name.startswith(prefix):
            print(bucket.name)


def getRegion(s3, response):
    unsorted = {}
    for bucket in response['Buckets']:
        r = s3.get_bucket_location(Bucket=bucket['Name'])
        unsorted[bucket['Name']] = r['LocationConstraint']
    for key in sorted(unsorted):
        print('{} is located in: {}'.format(key, unsorted[key]))


def ProcessBucket(response, s3Client, s3Resource, params):
    return null
