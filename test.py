import app
import unittest
from unittest import TestCase
import boto3


my_session = boto3.session.Session(profile_name='ec2_user', region_name='ap-south-1')
ec2_client = my_session.client(service_name='ec2')
regions = ec2_client.describe_regions()

list_of_regions = []
for re in regions['Regions']:
    list_of_regions.append(re['RegionName'])
print(list_of_regions)

def test_that_lambda_returns_correct_message():
    response = app.lambda_handler(list_of_regions,"test")
    assert response == ['i-06b8a0881adbbe353','i-0ff8895200ed6e703','i-07e753d8781f67663']

    
# if __name__ == '__main__':
#     unittest.main()