""" AWS S3 Utils

Utilities associated with managing S3 buckets on AWS. Must
have boto3 specs configured for these utilities to work.

Reference:
  https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
"""
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def upload_file(bucket_name: str, file_name: str, key: str):
    """ Upload file to S3 bucket. 

    :param bucket_name: name of bucket being used for upload
    :param file_name: file path to upload target
    :param key: s3 key for upload, 'test/myfile.txt'
    :return: Uploads file to S3 Bucket
    :rtype: None
    """
    try:
        s3 = boto3.client('s3')

        s3.upload_file(file_name, bucket_name, key)
        logger.info("Uploaded {} to {} using {}".\
                    format(file_name, bucket_name, key))

    except Exception as exc:
        logger.error("Issue with s3 upload: {}".format(file_name))
        logger.exception(exc)

def download_prove_file(repo_name: str, dirpath: str, bucket_name= "ds6050"):
    """ Download file from s3 bucket.

    :param repo_name: git repo name with owner included; 
                      tensorflow/tensorflow
    :param dirpath: directory path to place uncompressed 
                    file with repo owner

    :param bucket_name: name of s3 bucket
    :return: s3 object written to disk and True if present
    :rtype: bool
    """
    s3 = boto3.resource('s3')

    key = repo_name.replace("/", "__")
    file_path = dirpath + key + ".tar.gz"

    try:
        s3.Bucket(bucket_name).download_file(key, file_path)
        logger.info("Downloaded '{}'".format(file_path))
        return True

    except ClientError as ce:
        logger.info("Unable to find '{}' in s3 bucket '{}'".\
                     format(key, bucket_name))
        return False
        
        


