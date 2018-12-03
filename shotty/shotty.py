import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


@click.command()
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_instances(project):
    "List EC2 instances"
    instances = []

    if project:
        # print("here")
        filters = [{'Name':'tag:Project','Values':[project]}]
        # print(filters)
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        # ec2 = boto3.resource('ec2')
        # tag = i.tags(i.id,'project','value')

        # tags = {}
        # for t in i.tags():
        #     tags[t['Key']] = t['Value']

        print(','.join((i.id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name)))

    return


if __name__ == '__main__':
    list_instances()

