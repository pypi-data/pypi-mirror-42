""" AWS S3 Utils

Utilities associated with managing S3 buckets on AWS. Must
have boto3 specs configured for these utilities to work.

Reference:
  https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
"""
import logging

import boto3

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
        


