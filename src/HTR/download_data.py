from PIL import Image
from pathlib import Path
from config import IMAGE_PROCESSING_BUCKET, image_processing_s3_client


bucket_name = IMAGE_PROCESSING_BUCKET
s3_client = image_processing_s3_client


def download_data_from_s3(bucket_name, object_key, output_dir):
    filename = object_key.split("/")[-1]
    output_path = output_dir / filename
    if output_path.is_file():
        print(f"Image already downloaded: {filename}")
        return
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

def check_image(obj_key):
    image_name = obj_key.split("/")[-1]
    dir_path = Path(f"./data/Marieke/Normalisation-7/")
    image_path = dir_path / image_name
    if image_path.is_file():
        pass
    else:
        print(f"Image not found: {image_name}")

def get_images(prefix, output_dir):
    image_names = []
    obj_keys = list_obj_keys(prefix, s3_client, bucket_name)
    images = []
    for obj_key in obj_keys:
        image_name = obj_key.split("/")[-1]
        image_names.append(image_name)
        images = set(image_names)
        images_str = "\n".join(images)
    Path(f"./cropped_images.txt").write_text(images_str)
        
        # check_image(obj_key)

        # num += 1
        # image_names.append(obj_key)
        # download_data_from_s3(bucket_name, obj_key, output_dir)
        # print(f"Image {num}")
    
def convert_tif_to_jpg(image_dir, output_path):
    for tiff_path in image_dir.iterdir():
        try:
            image_name = tiff_path.name.split(".")[0]
            tiff_image = Image.open(tiff_path)
            if tiff_image.mode == 'CMYK':
                tiff_image = tiff_image.convert('RGB')
            result_fn = Path(f"{output_path}/{image_name}.jpg")
            if result_fn.is_file():
                continue
            tiff_image.save(result_fn, 'JPEG')
        except Exception as e:
            print(f"Error converting TIFF to JPEG: {e}")


def main():
    # prefix = "scam_cropped/PT/Manual3-20240515"
    prefix = "PT/cropped"
    batch_id = "Normalisation-7"
    # image_dir = Path(f"./data/Marieke/{batch_id}/")
    # output_path = Path(f"./data/Marieke/{batch_id}1/")
    # convert_tif_to_jpg(image_dir, output_path)
    output_dir = Path(f"./data/Marieke/{batch_id}/")
    output_dir.mkdir(parents=True, exist_ok=True)
    get_images(prefix, output_dir)

if __name__ == "__main__":
    main()