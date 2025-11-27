import uuid

import boto3
from django.conf import settings


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def generate_presigned_upload_url(filename: str, tenant_schema: str, content_type: str):
    """
    Generates a pre-signed S3 URL and object key for direct upload.
    """
    s3 = get_s3_client()

    key = f"{tenant_schema}/__temp__/chat_uploads/{uuid.uuid4()}_{filename}"

    # Generate a pre-signed PUT URL
    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=settings.AWS_S3_UPLOAD_EXPIRATION,
    )

    return {
        "upload_url": presigned_url,
        "file_url": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}",
        "key": key,
    }


def remove_temp_tag_from_s3_object(key: str) -> str:
    """
    Removes the 'temp=true' tag from an S3 object when message is sent.
    Returns the updated S3 object key.
    """
    s3 = get_s3_client()
    updated_key = key.replace("__temp__/", "")
    updated_url = (
        f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{updated_key}"
    )
    if key != updated_key:
        s3.copy_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            CopySource={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": key},
            Key=updated_key,
        )
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
    return updated_key, updated_url
