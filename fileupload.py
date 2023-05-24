import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def configureCreds():
    session = boto3.Session()
    credentials = session.get_credentials()


def upload(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, object_key)

upload('classroom-schedule', '/home/trent/test.txt', '/home/trent/test.txt')