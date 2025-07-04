import boto3

from src.files_api.s3.write_objects import upload_s3_object


def test_write_object_to_s3():
    """
    Test writing an object to S3.
    """

    TEST_BUCKET_NAME = "test-bucket-mlops-club-terete"
    Object_key = "test-object.txt"
    object_content = b"Hello, world!"
    content_type = "text/plain"
    s3_client = boto3.client("s3")
    s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=Object_key,
        file_content=object_content,
        content_type=content_type,
        s3_client=s3_client,
    )

    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=Object_key)
    assert response["ContentType"] == content_type
    assert response["Body"].read() == object_content
    response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
    for obj in response.get("Contents", []):
        s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])
    s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)
