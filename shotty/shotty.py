import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
        instances= []

        if project:
            filters = [{'Name':'tag:Project', 'Values':[project]}]
            instances = ec2.instances.filter(Filters=filters)
        else:
            instances = ec2.instances.all()

        return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="only instances for project(tag Project:<name>)")

def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {['Key']: t['Value'] for t in i.tags or []}
        print(i)
        print(', '.join((
            i.id,
            i.instance_type,
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))
        return

@instances.command('stop')
@click.option('--project', default=None, help='only instances for project')
def stop_instances(project):
    "stop EC2 instances"
    instances= []

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}....".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None, help='only instances for project')
def start_instances(project):
    "Start EC2 instances"
    instances= []

    instances = filter_instances(project)

    for i in instances:
        print("Startin {0}....".format(i.id))
        i.start()

    return



if __name__=='__main__':
    instances()
