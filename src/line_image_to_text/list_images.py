from pathlib import Path
from line_image_to_text.config import MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client


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


def main():
    s3_keys = ""
    prefix = "line_to_text/batch20/"
    image_names = get_image_name(prefix)
    for image_name in image_names:
        s3_keys += image_name + "\n"
    Path("./batch19.txt").write_text(s3_keys)


if __name__ == "__main__":
    main()
  