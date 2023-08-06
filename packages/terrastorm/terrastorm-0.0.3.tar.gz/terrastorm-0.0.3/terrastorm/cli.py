import os
import click
import subprocess
from pprint import pformat
from terrastorm.settings import conf, data
from terrastorm.services import TerrastormService

ts = TerrastormService(conf=conf)
OBJECT_TYPES = ('module', 'layer', 'environment')


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('path')
def setup(ctx, path):
    """
    setup a new project at a path
    """
    print('init a new project at "{}"'.format(path))
    resp = ts.initialize_project(path=path)
    click.echo('\nPlease place the following in ~/.terrastorm.yaml\n"""{}"""'.format(resp))

@cli.command()
@click.pass_context
def config(ctx):
    """
    show the current config
    """
    click.echo('\nYour current config is:\n"""{}"""'.format(pformat(data)))

@cli.command()
@click.pass_context
@click.argument('object_type', type=click.Choice(OBJECT_TYPES))
@click.argument('name')
def create(ctx, object_type, name):
    """
    Will create a new {}
    """.format(OBJECT_TYPES)
    print('add a new "{}" named "{}"'.format(object_type, name))
    resp = ts.create(object_type=object_type,
                     name=name)
    click.echo(resp)


@cli.command()
@click.pass_context
@click.argument('object_type', type=click.Choice(['service']))
@click.argument('environment', type=click.Choice(ts.environments()))
@click.argument('name')
def add(ctx, object_type, environment, name):
    """
    Will add a new service to the selected :environment based on :module and call it :name
    """
    print('add a new "{}" to "{}" named "{}"'.format(object_type, environment, name))
    resp = ts.create(object_type=object_type,
                     name=name,
                     environment=environment)
    click.echo(resp)


@cli.command()
@click.pass_context
@click.argument('environment', type=click.Choice(ts.environments()))
@click.argument('command', type=click.Choice(['apply', 'console', 'destroy', 'fmt', 'get', 'graph',
                                              'import', 'init', 'output', 'plan', 'providers',
                                              'push', 'refresh', 'show', 'taint', 'untaint', 'validate',
                                              'version', 'workspace', 'debug', 'force-unlock', 'state']))
@click.argument('services', nargs=-1)
def run(ctx, environment, command, services):
    """
    Will run a terraform command in the selected environment
    """
    resp = 'run "{}" in {} for {}'.format(command, environment, services)
    # click.echo(resp)
    resp = ts.run(command=command,
                  environment=environment,
                  services=set(services))
    for r in resp:
        code, msg, err = r.result()
        click.echo(msg)
        if code == 1:
            click.echo(err, err=True)    

@cli.command()
@click.pass_context
@click.argument('environment', type=click.Choice(ts.environments()))
@click.argument('command')
def cmd(ctx, environment, command):
    """
    Will execute a terraform command in the selected environment
    """
    resp = 'execute "{}" in {}'.format(command, environment)
    click.echo(resp)

    env_path = os.path.join(ts.conf.base.environments, environment)
    command = 'cd {};{}'.format(env_path, command)

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    click.echo(err if err else out, err=err==1)


cli.add_command(setup)
cli.add_command(config)
cli.add_command(create)
cli.add_command(add)
cli.add_command(run)

def run():
    cli(obj={})

if __name__ == '__main__':
    run()