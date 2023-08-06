import boto3
import time
from botocore.exceptions import ClientError
    
def launch_new_ec2(aws_conf, return_dns_name=False):
    '''Launch a new EC2 instance
    
    Args:
        aws_conf (deploy_utils.config.DefaultConfig): Configuration vals for AWS.
        return_connection (boolean, default=False): true to return both the instance and the connection
    
    Returns:
        varies: either the instance_id that was launched.
            or
            the instance_id that was launched and the public_dns_name
    '''

    boto3.setup_default_session(
        profile_name=aws_conf.get('aws_profile_name'),
        region_name=aws_conf.get('region')
    )
    ec2 = boto3.client('ec2')

    try:
        print('Launching new instance')
        response = ec2.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': aws_conf.get('block_device_map'),
                    'Ebs': {

                        'DeleteOnTermination': True,
                        'VolumeSize': int(aws_conf.get('volume_size')),
                        'VolumeType': 'gp2'
                    },
                },
            ],
            ImageId=aws_conf.get('ami_id'),
            InstanceType=aws_conf.get('instance_type'),
            KeyName=aws_conf.get('key_pair_name'),
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False
            },
            SecurityGroupIds=aws_conf.get('security_groups').split(',')
        )
        instance_id = response['Instances'][0]['InstanceId']
    except ClientError as e:
        print(e)

    # Check if it's up and running a specified maximum number of times
    max_retries = 10
    num_retries = 0
    status = 'pending'

    print('Launch successful, waiting until instance is running')
    while status == 'pending':
        if num_retries > max_retries:
            tear_down(instance_id)
            raise Exception('Maximum Number of Instance Retries Hit.  Did EC2 instance spawn correctly?')
        num_retries += 1
        print('Instance pending, waiting 10 seconds...')
        time.sleep(10)
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance_info = response['Reservations'][0]['Instances'][0]
        status = instance_info['Monitoring']['State']
        instance_public_dns_name = instance_info['PublicDnsName']
        if not instance_public_dns_name:
            status = 'pending'


    if return_dns_name:
        return instance_id, instance_public_dns_name
    else:
        return instance_id

def tear_down(instance_id):
    '''Terminates a EC2 instance and deletes all associated volumes.
    
    Args:
        instance_id (string): The ec2 instance id to terminate.
        conn (boto.ec2.connection.EC2Connection): Connection to region.
    '''
    
    print('Terminating instance')
    boto3.resource('ec2').Instance(instance_id).terminate()
