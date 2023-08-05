"""
    These are the sub-commands for a top level object added to the CLI group in 'cli.py'.
    The commands and options are implemented here and the logic behind them resides in the corresponding behavior file.
"""

from cli import pyke, behavior
import click

@click.group('microservice-version', help="A microservice-version is the docker image of a non visual widget, \
along with the details it needs to run such as, port number and Env variables.")
def microservice_version():
    pass

@click.command('ls')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--format', '-f', default='{id} {actualState} {versionNumber} {label} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--filter', default='')
@click.option('--page', default=1)
@click.option('--pagesize', default=100)
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def list(microservice, profile, format, json, **kwargs):
    behavior.MicroserviceVersionBehavior(profile=profile, format=format, json=json, **kwargs).list(microservice)

@click.command('start')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version', '-v', prompt=True, help='The version ID or the version-number')
@click.option('--format', '-f', default='{id} {actualState} {versionNumber} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def start(microservice, version, profile, format, json):
    behavior.MicroserviceVersionBehavior(profile=profile, format=format, json=json).start_stop("start", microservice, version)

@click.command('stop')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version', '-v', prompt=True, help='The version ID or the version-number')
@click.option('--format', '-f', default='{id} {actualState} {versionNumber} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def stop(microservice, version, profile, format, json):
    behavior.MicroserviceVersionBehavior(profile=profile, format=format, json=json).start_stop("stop", microservice, version)

@click.command('exec', help='Pass in a command to be run directly on the docker container.')
@click.argument('command')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version', '-v', prompt=True, help='The version ID or the version-number')
@click.option('--target', default="one", help='Run this command on "one" replica of the service or "all" replicas.' )
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def run(command, microservice, version, profile, target, json):
    behavior.MicroserviceVersionBehavior(profile=profile, json=json).run(microservice, version, command, target)

@click.command('logs')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version', '-v', prompt=True, help='The version ID or the version-number')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def logs(microservice, version, profile, json):
    behavior.MicroserviceVersionBehavior(profile=profile, json=json).logs(microservice, version)

@click.command('add')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--port', type=int, help='The port to connect to your microservice')
@click.option('--docker-image', '-image', type=str, help='The name (including the tag) of a docker image from the docker daemon. You must have docker running locally to use this option.')
@click.option('--microservice-file-path', '-path', type=click.Path(), help='The image must be a gzipped tar file. Ex: {file_name}.tar.gz')
@click.option('--from-version', '-fv', type=str, help="Take all values from an exsisting version and create a new version. \
Increment the major, minor or patch version by 1 with --major, --minor, --patch flags. Override any old values by passing them in as options.")
@click.option('--version', '-v', type=str, default=None, help="The version number of the new version")
@click.option('--patch', 'version_bump', flag_value='patch', default=True)
@click.option('--minor', 'version_bump', flag_value='minor')
@click.option('--major', 'version_bump', flag_value='major')
@click.option('--env-var', 'env', default=None, multiple=True, help="The environment variables to add to the docker image when it is run. It must be valid json wrapped in single quotes.")
@click.option('--label', '-l', type=click.Choice(['prod', 'dev', 'old']))
@click.option('--format', '-f', default='{id} {actualState} {versionNumber} {label} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def create(microservice, profile, port, microservice_file_path,\
    docker_image, from_version, version, version_bump, env, label, format, json):
    behavior.MicroserviceVersionBehavior(profile=profile, json=json).create(microservice, port,\
        microservice_file_path, docker_image, from_version, version, version_bump, env, label, format)

@click.command()
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version', '-v', prompt=True, help='The version ID or the version-number')
@click.option('--label', '-l', prompt=True)
@click.option('--format', '-f', default='{id} {versionNumber} {label} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def update(microservice, version, label, profile, format, json):
    behavior.MicroserviceVersionBehavior(profile=profile, json=json).update(microservice, version, label, format)

@click.command('rm')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--microservice', '-ms', prompt=True)
@click.option('--version-mask', '-vm', type=str, help="Delete versions with version numbers that match this version mask")
@click.option('--version', '-v', help='The version ID or the version-number')
@click.option('--format', '-f', default='{id} {versionNumber} {label} {createdAt}', help='The --format option takes the column name of the returned table wrapped in \
{} and returns only that column. It is not compatible with --json flag.')
@click.option('--json/--table', default=False, help='Return raw json from the platform.')
@pyke.auth.profile_context_required
def delete(microservice, version_mask, version, profile, format, json):
    behavior.MicroserviceVersionBehavior(profile=profile, json=json).delete(microservice, version, version_mask, format)

microservice_version.add_command(list)
microservice_version.add_command(create)
microservice_version.add_command(start)
microservice_version.add_command(stop)
microservice_version.add_command(delete)
microservice_version.add_command(update)
microservice_version.add_command(run)
microservice_version.add_command(logs)
