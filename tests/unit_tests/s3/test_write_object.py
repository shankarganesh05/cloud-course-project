import boto3,os
from moto import mock_aws
from src.files_api.s3.write_objects import upload_s3_object

# export AWS_ACCESS_KEY_ID='testing'
# export AWS_SECRET_ACCESS_KEY='testing'
# export AWS_SECURITY_TOKEN='testing'
# export AWS_SESSION_TOKEN='testing'
# export AWS_DEFAULT_REGION='us-east-1'


def point_away_from_aws():
    """
    Point away from AWS to use the moto library for testing.
    """
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@mock_aws
def test_write_object_to_s3():
    """
    Test writing an object to S3.
    """
    point_away_from_aws()
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
