#codeing:utf-8
import os
import shutil
import boto3
import zipfile

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        if not object_key.endswith(".zip"):
            continue
        object_dir = object_key[:object_key.rfind("/") + 1]
        s3_client.download_file(bucket_name, object_key, '/tmp/tmp.zip')
        try:
            shutil.rmtree('/tmp/zip')
        except:
            pass
        with zipfile.ZipFile('/tmp/tmp.zip', 'r') as zip_ref:
            zip_ref.extractall('/tmp/zip/')
        upload_folder(s3_client=s3_client, folder='/tmp/zip/', bucket_name=bucket_name, prefix=object_dir)
    return

def upload_folder(s3_client, folder, bucket_name, prefix):
    # get file list
    file_list = os.listdir(folder)

    # upload file and foler
    for file in file_list:
        file_path = folder + file
        if os.path.isdir(file_path):
            upload_folder(s3_client=s3_client, folder=file_path + '/', bucket_name=bucket_name, prefix=prefix)
        if os.path.isfile(file_path):
            key = (prefix + file_path.replace('/tmp/zip/', '')).encode('cp437').decode('utf-8')
            s3_client.upload_file(Bucket=bucket_name, Key=key, Filename=file_path)
            print(bucket_name)
            print(file_path.encode('cp437').decode('utf-8'))
            print(key)
    return