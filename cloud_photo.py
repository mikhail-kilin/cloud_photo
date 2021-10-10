import boto3
from boto3 import session
import sys, getopt
import os

bucket = "d23.itiscl.ru"

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[2:]

short_options = "p:a:"
long_options = ["path=", "album="]
arguments, values = getopt.getopt(argument_list, short_options, long_options)
path = ""
album = ""
for current_argument, current_value in arguments:
    if current_argument in ("-p", "--path"):
        path = current_value
    if current_argument in ("-a", "--album"):
        album = current_value

command = full_cmd_arguments[1]

session = boto3.session.Session()
s3Resource = session.resource(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

s3Client = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

if command == "upload":
    if path == "" or album == "":
        sys.stderr.write("error path or Album")
        sys.exit(1)
    files = os.listdir(path)
    images = list(filter(lambda x: x.lower().endswith('.jpg') or x.lower().endswith('.jpeg'), files))
    try: 
        for image in images:
            key = album+"/"+image
            while len(key.encode('utf-8')) > 1024:
                key = key[:-1]
            s3Client.upload_file(path+"/"+image, bucket, key)
    except:
        sys.stderr.write("error on uploading")
        sys.exit(1)

if command == "download":
    if path == "" or album == "":
        sys.stderr.write("error path or Album")
        sys.exit(1)
    try:
        os.mkdir(path)
    except: None
    try:
        for item in s3Resource.Bucket(bucket).objects.all():
            keys = item.key.split("/")
            if keys[0] == album:
                item.Object().download_file(path+"/"+keys[1])
    except:
        sys.stderr.write("error on downloading")
        sys.exit(1)

if command == "list":
    result = set()
    for item in s3Resource.Bucket(bucket).objects.all():
        keys = item.key.split("/")
        if album == "":
            if len(keys) > 1:
                result.add(keys[0])
        else:
            if keys[0] == album:
                result.add(keys[1])
    print(result)
