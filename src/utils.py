from pathlib import Path
import csv
from config import MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client


def write_csv(data, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def list_obj_keys(prefix, s3_client, bucket_name):
    obj_keys = []
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_keys.append(obj_key)
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return obj_keys


def get_image_name(prefix):
    image_names = []
    obj_keys = list_obj_keys(prefix=prefix, s3_client=monlam_ai_ocr_s3_client, bucket_name=MONLAM_AI_OCR_BUCKET)
    for obj_key in obj_keys:
        image_names.append(obj_key)
    return image_names


def list_images(batch_name):
    s3_keys = ""
    prefix = f"line_to_text/{batch_name}"
    image_names = get_image_name(prefix)
    for image_name in image_names:
        s3_keys += image_name + "\n"


def write_names(batch_name, image_names):
    s3_keys = ""
    for image_name in image_names:
        s3_keys += image_name + "\n"
    Path(f"./{batch_name}.txt").write_text(s3_keys)


def is_archived(s3_key, s3_client, Bucket):
    try:
        s3_client.head_object(Bucket=Bucket, Key=s3_key)
    except:
        return False
    return True

def add_row_to_csv(row, csv_path):
    if Path(csv_path).exists():
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    else:
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

def upload_to_s3(file_path, s3_key, s3_client=monlam_ai_ocr_s3_client, bucket_name=MONLAM_AI_OCR_BUCKET):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File uploaded successfully: {file_path}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")