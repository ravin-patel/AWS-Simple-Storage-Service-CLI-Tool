import os
import tempfile
import unittest
import boto3
import botocore
from moto import mock_s3
from BucketWorker import ProcessBucket
from Bucket import Bucket

BUCKET = "bucket"
PREFIX = "mock_folder"
@mock_s3
class TestS3(unittest.TestCase):
    def setUp(self):
        response = {'Buckets': [{'Name': 'fakeBucket12345', 'CreationDate': datetime.datetime(2019, 11, 15, 0, 38, 11, tzinfo=tzutc())}]}
        param = {
            'objectParams': {
                'size': False,
                'fileCount': False,
                'storage': False,
                'lastModified': False
            },
            'creationDate': True,
            'cost': True,
            'size_kb': False,
            'size_mb': False,
            'size_gb': False,
            'f': False
        }
        client = boto3.client(
            "s3",
            region_name="eu-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
    
        try:
            
            s3 = boto3.resource(
                "s3",
                region_name="eu-east-1",
                aws_access_key_id="fake_access_key",
                aws_secret_access_key="fake_secret_key",
                )
            res = ProcessBucket(response, client, s3, params)
            print(res)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = "{bucket} should not exist.".format(bucket=BUCKET)
            raise EnvironmentError(err)
        try:
           res = ProcessBucket(response, client, s3, params)
           print(res)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = 'Cant process bucket'
            raise EnvironmentError(err)
    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
        bucket = s3.Bucket(BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

if __name__ == "__main__":
    unittest.main()