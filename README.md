# AwsDeveloper

## CICD Pipeline for provisioning the resources on AWS using Jenkins pipeline

Step:1  (app.py)
------------------------------------------------------------------------------
create lambda function for listing out all EC2 instances in a particular region

import boto3.session

my_session = boto3.session.Session(profile_name='ec2_user', region_name='ap-south-1')
ec2_client = my_session.client(service_name='ec2')
regions = ec2_client.describe_regions()

list_of_regions = []
for re in regions['Regions']:
    list_of_regions.append(re['RegionName'])
print(list_of_regions)

def lambda_handler(event,handler):
    listinstance =[]
    for reg in list_of_regions:
        session = boto3.session.Session(profile_name='ec2_user', region_name=reg)
        ec2 = session.resource(service_name='ec2')
        print('list of ec2 instance in region'+ reg)
        instance = ec2.instances.all()
        for i in instance:
            #print(i.id,i.state['Name'])
            listinstance.append(i.id)
    
    return listinstance
    
 
 
Step:2 (test.py)
------------------------------------------------------------------------------
create test case for lambda function

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



Step:3 (instance.yml)
------------------------------------------------------------------------------
create cloudformation template for spinning ec2 instances

AWSTemplateFormatVersion: '2010-09-09'
Description: 'Master stack: PathToMasterStackFile'
Parameters:

Resources:
  stackset:
    Type: AWS::CloudFormation::StackSet
    Properties:
      Description: creation_of _ec2stack>
      ExecutionRoleName: <Role-arn>
      StackInstancesGroup:
        - DeploymentTargets:
            Accounts:
              - !Ref "AWS::AccountId"
          Regions:
            - ap-south-1
            - eu-west-1
      Parameters:
        - LatestAmiId:
            Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
            Default: '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
      PermissionModel: SELF_MANAGED
      StackSetName: instance_creation
      TemplateBody: !Sub
      - |
        ec2instance:
          Type: AWS::EC2::Instance
          Properties:
            ImageId: !ref LatestAmiId
            InstanceType: t2.micro
            KeyName: mind
            Monitoring: True
            Role: <iam--role--arn>
Outputs:
  stackid:       
    value: !GetAtt stackset.id
  
  

Step:4 (jenkinsfile)
------------------------------------------------------------------------------

pipeline {
    agent any
    stages {
        stage('git checkout') {
            steps{
                git branch: 'master',
                credentialsId: 'ashish097',
                url: 'url of jenkins file'
            }
        }
        stage('test lambda code') {
            steps {
                sh "pytest test.py"
            }
        }
        stage('Submit Stack') {
            steps {
                sh "aws cloudformation create-stack --stack-name ec2instance --template-body file://instance.yml"
            }
        }
    }
}
