from src.files_api.s3.read_objects import fetch_s3_object, fetch_s3_objects_using_page_token, fetch_s3_objects_metadata
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

def test_pagination(mocked_aws):
    """
    Test pagination when fetching objects from S3.
    """
    # Arrange
    s3_client = boto3.client("s3")
    for i in range(5):
        s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key=f"test-object-{i}.txt", Body=f"Test content-{i}")

    # Act
    files, next_token = fetch_s3_objects_metadata(bucket_name=TEST_BUCKET_NAME, max_keys=2)

    # Assert
    assert len(files) == 2
    assert files[0]['Key'] == 'test-object-0.txt'
    assert files[1]['Key'] == 'test-object-1.txt'

    # Fetch next page
    files, next_token = fetch_s3_objects_using_page_token(bucket_name=TEST_BUCKET_NAME,max_keys=2, continuation_token=next_token)
    
    assert len(files) == 2
    assert files[0]['Key'] == 'test-object-2.txt'
    assert files[1]['Key'] == 'test-object-3.txt'