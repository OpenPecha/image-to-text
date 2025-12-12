import boto3
from pathlib import Path
import subprocess
from botocore.exceptions import ClientError

def delete_file_from_s3(bucket_name, file_key):
    """
    Delete a file from an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket.
    :param file_key: The key (path) to the file in the S3 bucket.
    :return: True if the file was deleted, else False.
    """
    try:
        # Use subprocess to call AWS CLI's s3 rm command
        result = subprocess.run(
            ['aws', 's3', 'rm', f's3://{bucket_name}/{file_key}'],
            check=True,  # Will raise an error if the command fails
        )
        # If the command was successful
        print(result.stdout)
        print(f"File {file_key} deleted successfully from bucket {bucket_name}.")
        return True
    except subprocess.CalledProcessError as e:
        # Handle errors from the AWS CLI command
        print(f"Failed to delete {file_key} from bucket {bucket_name}. Error: {e.stderr}")
        return False


if __name__ == "__main__":
    bucket_name = "monlam.ai.ocr"
    file_paths = (Path("./data/Marieke/Correction-12/").iterdir())
    for file_path in file_paths:
        file_name = file_path.name
        file_key = f"Marieke/Correction-source/Correction-12/{file_name}"
        delete_file_from_s3(bucket_name, file_key)