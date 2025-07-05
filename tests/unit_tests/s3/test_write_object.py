import boto3,os
from moto import mock_aws
from src.files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME

# export AWS_ACCESS_KEY_ID='testing'
# export AWS_SECRET_ACCESS_KEY='testing'
# export AWS_SECURITY_TOKEN='testing'
# export AWS_SESSION_TOKEN='testing'
# export AWS_DEFAULT_REGION='us-east-1'

def test_write_object_to_s3(mocked_aws):
    """
    Test writing an object to S3.
    """
    # point_away_from_aws()
    # TEST_BUCKET_NAME = "test-bucket-mlops-club-terete"
    Object_key = "test-object.txt"
    object_content = b"Hello, world!"
    content_type = "text/plain"
    
    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=Object_key,
        file_content=object_content,
        content_type=content_type
    )
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=Object_key)
    assert response["ContentType"] == content_type
    assert response["Body"].read() == object_content