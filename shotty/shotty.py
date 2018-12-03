import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


def filter_instances(project):
    instances = []
    if project:

        filters = [{'Name': 'tag:Project', 'Values': [project]}]

        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


@click.group()
def instances():
    """Commands for Instances"""


@instances.command('list')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_instances(project):
    """List EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        tags = {}
        tags={t['Key']: t['Value'] for t in i.tags or []}

        print(', '.join(('Instance ID: '+ i.id, 'Instance Type: '+i.instance_type, 'Availability Zone: '+ i.placement['AvailabilityZone'], 'State: '+ i.state['Name'], 'Pub. DNS: '+ i.public_dns_name, 'Project Name:'+ tags.get('Project','<no project>'))))

    return


@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instancess(project):
    """Stop EC2 Instances"""
    instances = filter_instances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        i.stop()


@instances.command('start')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instancess(project):
    """Start EC2 Instances"""

    instances = filter_instances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))
        i.start()


if __name__ == '__main__':
    # list_instances()
    instances()
