
import boto3
import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
S3_BUCKET = os.getenv("S3_BUCKET", "nrve-audio-backend")  # Replace with your S3 bucket name
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID","AKIAW2R4M5ICL3KH7QOT" )
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY","E3DHJKy0Y1qz9aJFRl+aC/ThJVSOo3AXUSGw7KB5")

def upload_to_s3(file_path, s3_key):
    s3 = boto3.client("s3",
                      region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    s3.upload_file(file_path, S3_BUCKET, s3_key)
    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

