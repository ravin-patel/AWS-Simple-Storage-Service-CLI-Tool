# S3 CLI Tool

AWS S3 CLI Tool is used to get data of your s3 storage. This is done in python and utilizes the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) library

## Installation

Use the install.sh script to download all dependancies.

```bash
./install.sh
```

Alternatively you may also run [pip3](https://pip.pypa.io/en/stable/) to install the dependancies.

```bash
pip3 install -e .
```

## Getting Started

To connect to your AWS instance the tool will check for your user credentials via either a 'accessKeys.csv' file in the root folder. This can be generated and downloadable from the IAM dashboard.

If no 'accessKeys.csv' will also ask if AWS CLI is already configured and installed on your machine. If so it will look for your credentials in ~/.aws/credentials

If that also fails, the tool will then prompt the user to type or paste their credentials to connect

## Available Commands

**name**: returns the names of the buckets.
Use the optional argument _-f [filter string]_ to filter the bucket by name.

**size**: returns the total size of each bucket in bytes.
Use the optional argument _--kb --mb --gb_ to get the size in different units.

**creationDate**: returns the creation date of each bucket.

**fileCount**: returns the total number of files in each bucket.

**lastModified**: returns the name and time of the last modified object in each bucket.

**region**: returns each bucket grouped by their respective region.

**storage**: returns storage type of each object in the bucket.

## Usage

Example:

```bash
python3 s3cli size --kb -f <bucketNameFilterString>
python3 s3cli lastModified creationDate size --kb -f <bucketNameFilterString>
```

Sample Output:

```bash
ravinpatel$ python3 s3cli lastModified creationDate fileCount size --kb -f bucket-ravin1
Listing all buckets in: us-east-2
bucket-ravin1
|__ Size: 670.287 kb
|__ File Count: 8
|__ Creation Date: Fri Nov 15 00:38:11 2019
|__ Last Modified: reese.jpeg -- Modified at: 2019-11-23 21:17:33
bucket-ravin123
|__ Size: 19234.623 kb
|__ File Count: 1101
|__ Creation Date: Sat Nov 23 21:47:53 2019
|__ Last Modified: rnd2/file080.txt -- Modified at: 2019-11-23 22:22:18
```
