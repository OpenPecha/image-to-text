from pathlib import Path
from config import IMAGE_PROCESSING_BUCKET, image_processing_s3_client


bucket_name = IMAGE_PROCESSING_BUCKET
s3_client = image_processing_s3_client


def download_data_from_s3(bucket_name, object_key, output_dir):
    filename = object_key.split("/")[-1]
    output_path = output_dir / filename
    try:
        s3_client.download_file(bucket_name, object_key, output_path)
        print(f"Image downloaded successfully: {filename}")
    except Exception as e:
        print(f"An error occurred during download: {e}")



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


def get_images(prefix, output_dir):
    image_names = []
    obj_keys = list_obj_keys(prefix, s3_client, bucket_name)
    for obj_key in obj_keys:
        image_names.append(obj_key)
        download_data_from_s3(bucket_name, obj_key, output_dir)


def main():
    prefix = "PT/Corr3-20242604/"
    batch_id = "Correction-3"
    output_dir = Path(f"./data/Marike/{batch_id}/")
    get_images(prefix, output_dir)

if __name__ == "__main__":
    main()