import boto3
import os
import pytz
from datetime import datetime, timedelta

LOCAL_FOLDER = '/media1' # Folder that needs to be backed up to S3
DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'
DEFAULT_START_DATE = datetime.strptime('1970-01-01 00:00:00+00:00', DATE_FORMAT) # Default date when there is no file present in S3
AWS_PROFILE = 'home-server'
BUCKET_NAME = ''
BUCKET_PATH = 'home-server'
REGION = 'us-east-1'

boto3.setup_default_session( region_name=REGION, profile_name=AWS_PROFILE),

def get_last_uploaded_file(bucket_name, bucket_path):
    last_uploaded_time = DEFAULT_START_DATE
    # Create an S3 client
    s3 = boto3.client('s3')

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=bucket_path)

    # Check if any objects are available
    if response and 'Contents' in response:
        # Sort the objects by the LastModified timestamp in descending order
        sorted_objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)

        if len(sorted_objects) > 1:
            # Retrieve the key (filename) of the last uploaded file
            last_uploaded_time = sorted_objects[0]['LastModified']

            return last_uploaded_time
        else:
            print("No files present in folder" + bucket_path)
    else:
        print("No objects found in the bucket.")

    return last_uploaded_time

def upload_file_multipart(bucket_name, bucket_path, file_paths):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        for file_path in file_paths:
            bucket_file = bucket_path + '/' + os.path.basename(file_path)
            # Initiate the multipart upload
            response = s3.create_multipart_upload(Bucket=bucket_name, Key=bucket_file, StorageClass='DEEP_ARCHIVE')

            # Retrieve the upload ID from the response
            upload_id = response['UploadId']

            # Open the file for reading
            with open(file_path, 'rb') as file:
                # Set the part size (5MB in this example)
                part_size = 5 * 1024 * 1024

                # Initialize part number and parts list
                part_number = 1
                parts = []

                while True:
                    # Read a part-sized chunk from the file
                    data = file.read(part_size)

                    # Break if end of file
                    if not data:
                        break

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

                print("File upload completed.")
                print("Object URL:", response['Location'])

    except Exception as e:
        # Abort the multipart upload in case of any exception
        s3.abort_multipart_upload(Bucket=bucket_name, Key=bucket_file, UploadId=upload_id)
        print("File upload failed:", str(e))


def find_files_modified_after(directory, after_date):
    file_paths = []

    # Iterate over the files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Get the modification timestamp of the file
            modification_time = datetime.fromtimestamp(os.path.getmtime(file_path), pytz.utc)
            # Compare the modification time with the threshold
            if modification_time > after_date:
                print(file_path)
                file_paths.append(file_path)

    return file_paths

last_s3_file_time = get_last_uploaded_file(BUCKET_NAME, BUCKET_PATH)
file_paths = find_files_modified_after(LOCAL_FOLDER, last_s3_file_time)
upload_file_multipart(BUCKET_NAME, BUCKET_PATH, file_paths)