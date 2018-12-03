import boto3
import click
import botocore

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
def cli():
    """Shotty manages snapshots"""


@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""


@snapshots.command('list')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_snapshots(project):
    """List Snapshots"""

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join(("Snapshot ID: "+ s.id, "Volume ID: "+ v.id, "Instance ID: "+ i.id, "State: "+ s.state, "Progress: "+ s.progress, "Start Time: " + s.start_time.strftime('%c'))))

    return


@cli.group('volumes')
def volumes():
    """Commands for Volumes"""


@volumes.command('list')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_volumes(project):
    """List Volumes"""

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(', '.join(("Volume Id: " + v.id, "Instance Id: " + i.id, "Volume State:" + v.state,
                             "Volume Size: " + str(v.size) + 'GiB', v.encrypted and 'Encrypted' or 'Not Encrypted')))
    return


@cli.group('instances')
def instances():
    """Commands for Instances"""


@instances.command('snapshot')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def create_snapshots(project):
    """Create Snapshots for EC2 instances"""

    instances = filter_instances(project)
    for i in instances:
        print('Stopping {0}...'.format(i.id))

        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print('Creating snapshot of {0}'.format(v.id))
            v.create_snapshot(Description='Created By snapshot-3000')
        print('Starting {0}...'.format(i.id))
        i.start()
        i.wait_until_running()
    print('Jobs Done')
    return

@instances.command('list')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_instances(project):
    """List EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        tags = {}  # dictionary comprehension used here
        tags = {t['Key']: t['Value'] for t in i.tags or []}

        print(', '.join(('Instance ID: ' + i.id, 'Instance Type: ' + i.instance_type,
                         'Availability Zone: ' + i.placement['AvailabilityZone'], 'State: ' + i.state['Name'],
                         'Pub. DNS: ' + i.public_dns_name, 'Project Name:' + tags.get('Project', '<no project>'))))

    return


@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instancess(project):
    """Stop EC2 Instances"""
    instances = filter_instances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print('Could not stop {0}. '.format(i.id) + str(e))
            continue



@instances.command('start')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instancess(project):
    """Start EC2 Instances"""

    instances = filter_instances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print('Could not start {0}. '.format(i.id) + str(e))
            continue


if __name__ == '__main__':
    # list_instances()
    cli()
