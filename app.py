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