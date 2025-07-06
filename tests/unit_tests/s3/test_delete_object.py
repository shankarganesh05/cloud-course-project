from src.files_api.s3.delete_objects import delete_s3_object
from tests.consts import TEST_BUCKET_NAME
import boto3

def test_delete_object_from_s3(mocked_aws):
    """
    Test deleting an object from S3.
    """
    # Arrange
    s3_client = boto3.client("s3")
    object_key = "test-object.txt"
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key=object_key, Body=b"Test content")

    # Act
    delete_s3_object(bucket_name=TEST_BUCKET_NAME, object_key=object_key)

    # Assert
    response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
    assert not response.get("Contents") or len(response["Contents"]) == 0
    