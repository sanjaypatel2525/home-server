import boto3
import os
from datetime import datetime

print("Starting the s3 upload")

LOCAL_FOLDER = '/media' # Folder that needs to be backed up to S3
DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'
AWS_PROFILE = 'home-server'
BUCKET_NAME = '<BBUCKET_NAME>'
BUCKET_PATH = 'home-server'
REGION = 'us-east-1'

boto3.setup_default_session( region_name=REGION, profile_name=AWS_PROFILE),

def get_last_uploaded_file(bucket_name, bucket_path):
    s3_files = []
    # Create an S3 client
    s3 = boto3.client('s3')

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=bucket_path)

    # Check if any objects are available
    if response and 'Contents' in response:
        # Sort the objects by the LastModified timestamp in descending order
        sorted_objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)
        s3_files = [file['Key'].replace(bucket_path + "/", "") for file in sorted_objects]
        log("Files in s3" + str(s3_files))
    else:
        log("No objects found in the bucket.")

    return s3_files

def upload_file_multipart(bucket_name, bucket_path, file_paths):
    # Create an S3 client
    s3 = boto3.client('s3')
    # Set the part size (1GB in this example)
    part_size = 1024 * 1024 * 1024

    try:
        for file_path in file_paths:
            bucket_file = bucket_path + '/' + os.path.basename(file_path)
            log("Uploading file " + file_path)

            if os.path.getsize(file_path) == 0:
                log("File size is zero (empty)")
                continue

            # Open the file for reading
            with open(file_path, 'rb') as file:
                # Initialize part number and parts list
                part_number = 1
                parts = []

                # Initiate the multipart upload
                response = s3.create_multipart_upload(Bucket=bucket_name, Key=bucket_file, StorageClass='DEEP_ARCHIVE')

                # Retrieve the upload ID from the response
                upload_id = response['UploadId']

                while True:
                    # Read a part-sized chunk from the file
                    data = file.read(part_size)

                    # Break if end of file
                    if not data:
                        break

                    log("Uploading part :" + str(part_number) + " of file : " + str(file_path))

                    # Upload the part
                    response = s3.upload_part(
                        Bucket=bucket_name,
                        Key=bucket_file,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=data
                    )

                    # Retrieve the ETag for the uploaded part
                    part_etag = response['ETag']

                    # Add the part number and ETag to the parts list
                    parts.append({'PartNumber': part_number, 'ETag': part_etag})

                    # Increment the part number
                    part_number += 1

                # Complete the multipart upload
                response = s3.complete_multipart_upload(
                    Bucket=bucket_name,
                    Key=bucket_file,
                    UploadId=upload_id,
                    MultipartUpload={'Parts': parts}
                )

                log("File upload completed.")
                log("Object URL:" + str(response['Location']))

    except Exception as e:
        # Abort the multipart upload in case of any exception
        s3.abort_multipart_upload(Bucket=bucket_name, Key=bucket_file, UploadId=upload_id)
        log("File upload failed:" + str(e))


def find_files_modified_after(directory, files_in_s3):
    log("fetching file from local folder :" + directory)

    items = os.listdir(directory)
    files = [item for item in items if os.path.isfile(os.path.join(directory, item)) and item not in files_in_s3]
    sorted_files = sorted(files, key=lambda x: os.stat(os.path.join(directory, x)).st_mtime)

    log("Files to be uploaded " + str(sorted_files))

    return [(directory + '/' + file) for file in sorted_files]

def log(msg) :
    print("[" + datetime.now().strftime(DATE_FORMAT) + "] " + msg)

files_in_s3 = get_last_uploaded_file(BUCKET_NAME, BUCKET_PATH)

file_paths = find_files_modified_after(LOCAL_FOLDER, files_in_s3)

upload_file_multipart(BUCKET_NAME, BUCKET_PATH, file_paths)

