import unittest
import boto
from boto.s3.key import Key
from moto import mock_s3
import boto3


class TestS3(unittest.TestCase):
    mock_s3 = mock_s3()

    def setUp(self):
        self.mock_s3.start()
        self.location = "eu-west-1"
        self.bucket_name = 'fakebucket1-ravin'
        self.key_name = 'mock/fake_fake/test.json'
        self.key_contents = 'This is test data.'
        s3 = boto.connect_s3()
        bucket = s3.create_bucket(self.bucket_name, location=self.location)
        k = Key(bucket)
        k.key = self.key_name
        k.set_contents_from_string(self.key_contents)

    def tearDown(self):
        self.mock_s3.stop()

    def test_s3_boto3(self):
        s3 = boto3.resource('s3', region_name=self.location)
        bucket = s3.Bucket(self.bucket_name)
        assert bucket.name == self.bucket_name
        # retrieve already setup keys
        keys = list(bucket.objects.filter(Prefix=self.key_name))
        assert len(keys) == 1
        assert keys[0].key == self.key_name
        # update key
        s3.Object(self.bucket_name, self.key_name).put(Body='new')
        key = s3.Object(self.bucket_name, self.key_name).get()
        assert 'new' == key['Body'].read()
