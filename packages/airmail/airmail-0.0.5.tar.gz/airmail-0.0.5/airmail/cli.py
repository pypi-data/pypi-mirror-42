
import os
import sys
import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix='AIRMAIL')

class Context(object):
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def preamble_log(self, preamble, value):
        click.echo(click.style(preamble, fg="blue", bold=True) + ": " + value)

    def warn_log(self, msg):
        click.echo(click.style("Warn", fg="yellow", bold=True) + ": " + msg)

    def verbose_log(self, msg):
        if self.verbose:
            click.echo(click.style("Verbose", fg="white", bold=True) + ": " + msg)

    def info_log(self, msg):
        click.echo(click.style("Info", fg="green", bold=True) + ": " + msg)

    def add_line_break(self):
        click.echo("\n")

    def err_log(self, msg, *args):
        if args:
            msg %= args
        click.echo(click.style("Error: ", fg="red", bold=True) + msg)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class AirMailCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('airmail.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli

@click.command(cls=AirMailCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--profile', help='The AWS profile to use', default=lambda: os.environ.get('AWS_PROFILE', None))
@click.option('-e', '--env', help='The environment to target', default=lambda: os.environ.get('ENV', ''))
@click.option('-d', '--dry-run', help='Commands run with this flag will not result in actual changes to your AWS configuration', default=lambda: os.environ.get('DRY_RUN', False))
@click.option('-v', '--verbose', help='Run commands with verbose logging', default=lambda: os.environ.get('VERBOSE', False))
@pass_context
def cli(ctx, profile, env, dry_run, verbose):
    """A CLI for getting code into the cloud"""
    ctx.env = env
    ctx.profile = profile
    ctx.dry_run = bool(dry_run)
    ctx.verbose = bool(verbose)
