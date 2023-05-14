import boto3
import os
import gzip
import glob
import json
import tarfile
import math
from datetime import datetime, timedelta
from PIL import Image
from pillow_heif import register_heif_opener

ROOT = '' #TODO set value
BASE_PATH = ROOT + "\\photobackup\\media\\"
CONFIG_FILE = BASE_PATH + "config.json"
CONFIG = {}
SCAN_TILL = datetime.now() - timedelta(hours=1)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
VAULT_NAME = 'mynasbackup'
boto3.setup_default_session(profile_name='nasuser')
MEDIA_PATH = ROOT + '\\photobackup\\media\\'

cachedFilesList = []


def write_config():
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(CONFIG, outfile)
    print("Writing Json" + str(CONFIG))


def read_config():
    global CONFIG
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as infile:
            CONFIG = json.load(infile)
    else:
        CONFIG = {"lastScan":  (datetime.now() - timedelta(weeks=30*54)).strftime(DATE_FORMAT)} #start with very old date

    print("Read Json" + str(CONFIG))


def get_files_modified_after_and_before(path):
    global cachedFilesList
    if len(cachedFilesList) > 0:
        return cachedFilesList

    print("Getting list of files to be uploaded")
    for root, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            fromTime = datetime.strptime(CONFIG['lastScan'], DATE_FORMAT)
            if fromTime < modified_time < SCAN_TILL:
                cachedFilesList.append(file_path)
                print(file_path)

    print("Printed all the files that would be uploaded")
    return cachedFilesList


def convert_heic_to_jpg():
    print("Going to conver Heic to Jpg")
    if len(cachedFilesList) > 0:
        for input_file_path in cachedFilesList:
            if input_file_path.endswith('.HEIC'):
                # Open the HEIC file
                image = Image.open(input_file_path)

                # Save the image as JPEG
                jpegPath = input_file_path + ".jpeg"
                if not os.path.exists(jpegPath):
                    image.save(jpegPath, 'JPEG')
                    print(input_file_path)
    print("Printed all the files that are converted to jpeg")


def compress_file():
    # Check if there are any input files to compress
    if cachedFilesList:
        # Set up the output gzip file path
        output_file_path = ROOT + '\\photobackup_' + SCAN_TILL.strftime('%Y-%m-%dT%H-%M-%SZ') + '.tar.gz'
        print("creating compressed file at location" + output_file_path)

        # Create a tar file of all input files
        with tarfile.open(output_file_path, 'w:gz') as output_file:
            for input_file_path in cachedFilesList:
                output_file.add(input_file_path)

    print("compression complete at location file size is" + str(os.path.getsize(output_file_path)))
    return output_file_path


def upload_to_glacier(file_path):
    # Set up the S3 Glacier client
    glacier = boto3.client('glacier')

    # Set up the multipart upload parameters
    part_size = 1024 * 1024 * 100  # 100MB
    multipart_upload_id = glacier.initiate_multipart_upload(vaultName=VAULT_NAME, archiveDescription='My Archive Description', partSize=str(part_size))['uploadId']

    # Start the multipart upload
    with open(file_path, 'rb') as f:
        file_size = os.path.getsize(file_path)
        num_parts = int(math.ceil(file_size / float(part_size)))

        # Upload each part
        for i in range(num_parts):
            part_start = part_size * i
            part_end = min(part_start + part_size, file_size)
            part_size = part_end - part_start
            response = glacier.upload_multipart_part(vaultName=VAULT_NAME, uploadId=multipart_upload_id,
                                                     body=f.read(part_size),
                                                     range='bytes {}-{}/*'.format(part_start, part_end))

    # Complete the multipart upload
    glacier.complete_multipart_upload(vaultName=VAULT_NAME, uploadId=multipart_upload_id, archiveSize=str(file_size),
                                      checksum=response['checksum'])


read_config()
get_files_modified_after_and_before(MEDIA_PATH)
register_heif_opener()
convert_heic_to_jpg()
zip_path = ROOT + "\\photobackup_2023-04-23T21-50-32Z.tar.gz" #compress_file()
upload_to_glacier(zip_path)
CONFIG['lastScan'] = SCAN_TILL.strftime(DATE_FORMAT)
writeConfig(CONFIG)
