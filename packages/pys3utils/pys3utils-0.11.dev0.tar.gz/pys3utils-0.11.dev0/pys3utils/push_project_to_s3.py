"""
Module to download git repo and upload it to Amazon s3
Configure the bucket, and git url using the settings file
Ths also requires AWS credentials to be set up in a file (or using AWS CLI):
Unix: ~/.aws/credentials
Windows: C:\\Users\\Username\\.aws\\credentials
In this file put the following:
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
[default]
region=us-east-1
"""

import os
import boto3
import settings
import shutil
import errno, stat
from os import listdir
from os.path import isdir
from mimetypes import MimeTypes
from git import Repo
import logging
import sys
import time
import uuid


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_s3_bucket(bucket_prefix, s3_connection):
    """ Create an s3 bucket in your current region


    """
    session = boto3.session.Session()
    current_region = session.region_name
    if current_region == 'us-east-1':
        location_constraint = 'us-west-2'
    else:
        location_constraint = region
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': location_constraint})
    print(bucket_name, current_region)
    return bucket_name, bucket_response


def upload_file(file, **kwargs):
    """
    uploads a file to s3
    """
    if os.path.getmtime(file) < os.path.getmtime(kwargs['time_stamp_file']):
        return None

    # Replace windows slashes with unix slashes
    local_key = file.replace(kwargs['master_directory'], "")
    key = local_key.replace("\\", "/")
    print(key)
    # Remove first /
    if key.startswith("/"):
        key = key[1:]
    print('uploading {} with relative path {} in s3...'.format(file, key))
    res = kwargs['bucket'].Object(key).upload_file(file)
    print('s3 returned :', res)
    return res


def upload_dir(path, **kwargs):
    """
    Uploads directory recursively to s3
    """
    for file in listdir(path):

        filepath = os.path.join(path, file)
        if isdir(filepath) is True:
            upload_dir(filepath, **kwargs)
        else:
            upload_file(filepath, **kwargs)



def remove_readonly(func, path, excinfo):
    """
    Changes permissions on files that can't be deleted
    by shutil.rmtree
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    if not sys.argv[1]:
        logger.critical('You must provide a directory to push!')
        exit(1)

    directory = os.path.abspath(sys.argv[1])
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(sys.argv[2])
    syncfile = os.path.join(directory,'.s3_sync_timestamp')
    try:
        print("uploading directory {}".format(directory))
        print('-----------------------------------------')
        with open(syncfile, 'w+') as f:
            ts = time.time()
            f.write('last updated/pushed to s3:'+ str(ts))

        upload_dir(directory, bucket=bucket, master_directory=directory, time_stamp_file=syncfile)

    except Exception as ex:
        print(ex)

    return

if __name__ == "__main__":
    main()

# OLD for cloning and pushing
#
# # Create temp directory
# print("Creating temporary directory %s" % settings.TEMP_DIRECTORY)
# if not os.path.exists(settings.TEMP_DIRECTORY):
#     os.makedirs(settings.TEMP_DIRECTORY)
# # Clone repository to temp directory
# print("Cloning repository from %s" % settings.GIT_URL)
# Repo.clone_from(settings.GIT_URL, settings.TEMP_DIRECTORY)
#
# # Uploads contents of temp directory to s3
# print("Uploading to S3")
# upload_dir(settings.TEMP_DIRECTORY)
#     finally:
#         # Deletes temporary directory
#         print("Deleting temporary directory and contents")
#         shutil.rmtree(settings.TEMP_DIRECTORY, onerror=remove_readonly)