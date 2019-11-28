import boto3
import sys
import botocore
from Bucket import Bucket
import datetime
from datetime import datetime, timedelta


def IsBucketNameValid(name, prefix):
    return name.startswith(prefix)


def ProcessBucket(response, s3Client, s3Resource, params):
    result = {}
    for bucket in response['Buckets']:
        # checks if the filter flag exists  and if the filter flag is a valid name
        if (params['f'] and IsBucketNameValid(bucket['Name'], params['f'])) or (params['f'] is None):
            currentBucket = Bucket()  # instantiate new Bucket
            currentBucket.name = bucket['Name']  # set name attribute
            currentBucket.region = s3Client.get_bucket_location(
                Bucket=currentBucket.name)['LocationConstraint']  # set region attribute
            # set creation date attribute
            currentBucket.creationDate = bucket['CreationDate'].ctime()
            # checks if there are ANY object level data requested in the argument
            if (any(param == True for param in params['objectParams'].values())):
                ProcessBucketObjects(
                    currentBucket, bucket, params['objectParams'], s3Client, s3Resource)

            # insert bucket, all relevant data should be populated
            # check to see whether the region is already in result if so group them together, otherwise instantiate a list within a dict like:
            # result = {Key=RegionName, Val = [This is a list of buckets, append current one]}
            if currentBucket.region in result.keys():
                result[currentBucket.region].append(currentBucket)
            else:
                result[currentBucket.region] = [currentBucket]

    return result


def ProcessBucketObjects(bucketObj, bucket, params, s3Client, s3Resource):
    # Object level parameter processing
    format = '%Y-%m-%d %H:%M:%S+00:00'  # datetime formating
    totalSize = 0
    fileCount = 0
    lastModifiedDate = datetime(1900, 1, 1, 0)
    lastModifiedObj = ""
    # using paginator incase their are over 1000 objects in the bucket
    paginator = s3Client.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=bucket['Name'])
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:  # iterate through the objects
                fileCount += 1
                dt = obj['LastModified']
                bucketObj.storage[obj['Key']] = [obj['StorageClass']]
                totalSize += obj['Size']
                # checks if the current objects last modified date is greater than lastModifiedDate
                if(datetime.strptime(str(dt), format) > lastModifiedDate):
                    lastModifiedDate = datetime.strptime(str(dt), format)
                    lastModifiedObj = obj['Key']
            # sets the bucket class attributes based on the returned values
            bucketObj.fileCount = fileCount
            bucketObj.size_bytes = totalSize
            bucketObj.lastModifiedDate = lastModifiedDate
            bucketObj.lastModifiedFile = lastModifiedObj


def getCost(client):


    # use the bota3 lib to get the cost/usage
    start = datetime.now() - timedelta(days=15)
    end = datetime.now() + timedelta(days=2)
    res = client.get_cost_and_usage(TimePeriod={
         'Start': start.strftime('%Y-%m-%d'),
         'End': end.strftime('%Y-%m-%d')
        },Granularity = 'MONTHLY', 
        Metrics = ["BlendedCost", "UnblendedCost", "UsageQuantity"])
    
    print(res)
    buckets = dict()
    for x in res["ResultsByTime"][0]["Groups"]:
        metrics = x["Metrics"]
        buckets[x["Keys"][0]] = float(metrics["BlendedCost"]["Amount"]) + float(
            metrics["UnblendedCost"]["Amount"]) + float(metrics["UsageQuantity"]["Amount"])
    print(buckets)
