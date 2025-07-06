from src.files_api.s3.read_objects import fetch_s3_object
from tests.consts import TEST_BUCKET_NAME
import boto3

def test_read_object_from_s3(mocked_aws):
    """
    Test reading an object from S3.
    """
    # Arrange
    s3_client = boto3.client("s3")
    object_key = "test-object.txt"
    expected_content = b"Test content"
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key=object_key, Body=expected_content)

    # Act
    response = fetch_s3_object(bucket_name=TEST_BUCKET_NAME, object_key=object_key)

    # Assert
    assert response['Body'].read() == expected_content