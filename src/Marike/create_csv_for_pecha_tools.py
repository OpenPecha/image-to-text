from pathlib import Path
import jsonlines
import csv
import requests
from utils import add_row_to_csv
from config import PAGE_CROPPING_BUCKET, page_cropping_s3_client, MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client

bucket_name = PAGE_CROPPING_BUCKET
s3_client = page_cropping_s3_client

import boto3

def download_image_from_s3(bucket_name, object_key):
    filename = object_key.split("/")[-1]
    output_path = Path(f"./data/Marike/Manual-1/{filename}")
    try:
        s3_client.download_file(bucket_name, object_key, output_path)
        print(f"Image downloaded successfully: {filename}")
    except Exception as e:
        print(f"An error occurred during download: {e}")


def get_url_for_correction(image_url):
    new_image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/Marieke/Correction/Correction-1/{image_url[21:]}"
    return new_image_url


def create_csv_for_correction(jsonl_path, csv_path):
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, csv_path)
    ids = []
    with jsonlines.open(jsonl_path) as reader:
        for obj in reader:
            id = obj["id"]
            if id in ids:
                continue
            state = "transcribing"
            group_id = 1
            batch_id = "Correction-1"
            inference_transcript = obj["user_input"]
            image_url = get_url_for_correction(obj["image_url"])
            format = "line"
            row = [id, group_id, batch_id, state, inference_transcript,image_url, format]
            add_row_to_csv(row, csv_path)
            row = []


def get_new_url(image_url):
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": image_url},
        ExpiresIn=31536000
    )
    return new_image_url

def download_image(image_url, image_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(response.content)

def download_images(jsonl_path):
    with jsonlines.open(jsonl_path) as reader:
        for obj in reader:
            object_key = obj["image_url"]
            download_image_from_s3(bucket_name, object_key)
            # image_name = image_url.split("/")[-1]
            # image_path = image_dir / image_name
            # download_image(new_image_url, image_path)

def create_csv_for_manual(image_paths):
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    csv_path = Path(f"./data/Marike/Manual-1.csv")
    add_row_to_csv(headers, csv_path)
    for image_path in image_paths:
        id = image_path.name
        group_id = 2
        batch_id = "Manual-1"
        state = "transcribing"
        inference_transcript = ""
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/Marieke/Manual/Manual-1/{id}"
        format = "page"
        row = [id, group_id, batch_id, state, inference_transcript,image_url, format]
        add_row_to_csv(row, csv_path)

def main():
    # jsonl_path = Path(f"./data/Marike/Correction-1.jsonl")
    # csv_path = Path(f"./data/Marike/Correction-1.csv")
    # create_csv_for_correction(jsonl_path, csv_path)
    image_paths = list(Path(f"./data/Marike/Manual-1/").iterdir())
    create_csv_for_manual(image_paths)


if __name__ == "__main__":
    main()

