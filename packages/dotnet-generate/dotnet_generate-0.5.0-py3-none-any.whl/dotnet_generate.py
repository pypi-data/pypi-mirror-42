import glob
import re
import os
import subprocess

import click

test_run = False


@click.group(name="dotnet-generate")
def cli():
    """
    Tool for generating dotnet code.

    For additional help pass --help to subcommands.
    """
    pass


@click.command(name="migrate")
@click.argument('name')
@click.option('--update', '-u', is_flag=True, help="If set updates the db")
@click.option('--mvc', '-m', is_flag=True, help="If set create mvc controllers")
@click.option('--api', '-a', is_flag=True, help="If set create api controllers")
@click.option('--try', '-t', 'try_run', is_flag=True,
              help="doesn't actually run any commands, just prints commands to console.")
def migrate(name, update, mvc, api, try_run):
    """Migrate the db."""
    global test_run
    test_run = try_run
    cmd = f"dotnet ef migrations add {name} --project DAL --startup-project WebApp"
    click.echo(_run_shell_comand(cmd))
    if update:
        _update()
    if mvc:
        _create_MVC_controllers()
    if api:
        _create_API_controllers()


@click.command(name="update")
def update():
    """Update the database."""
    _update()


@click.command(name="mvc")
def create_MVC_controllers():
    """Create MVC controllers"""
    _create_MVC_controllers()


@click.command(name="api")
def create_API_controllers():
    """Create API controllers"""
    _create_API_controllers()


def _update():
    cmd = "dotnet ef database update --project DAL --startup-project WebApp"
    click.echo(_run_shell_comand(cmd))


def _create_MVC_controllers():
    db_sets = _find_db_sets()
    _chdir("WebApp/")
    for (model, plural) in db_sets:
        cmd = f"dotnet aspnet-codegenerator controller -name {plural}Controller -actions -m {model} -dc AppDbContext -outDir Controllers --useDefaultLayout --useAsyncActions --referenceScriptLibraries -f"
        result = _run_shell_comand(cmd)
        click.echo(result)
    _chdir("../")


def _create_API_controllers():
    db_sets = _find_db_sets()
    _chdir("WebApp/")
    for (model, plural) in db_sets:
        cmd = f"dotnet aspnet-codegenerator controller -name {plural}Controller -actions -m {model} -dc AppDbContext -outDir Api/Controllers -api --useAsyncActions -f"
        result = _run_shell_comand(cmd)
        click.echo(result)
    _chdir("../")


def _find_db_sets():
    context = glob.glob("DAL/*Context.cs")
    if not context:
        click.echo("AppDbContext.cs not found", err=True)
        return []
    with open(context[0]) as f:
        db_context = f.read()
    return re.findall(r"DbSet<([a-zA-Z]*)>\s([a-zA-Z]*)\s", db_context)


def _run_shell_comand(cmd):
    if test_run:
        return cmd
    result = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')


def _chdir(path):
    if test_run:
        click.echo("cd " + path)
    else:
        os.chdir(path)


cli.add_command(migrate)
cli.add_command(update)
cli.add_command(create_API_controllers)
cli.add_command(create_MVC_controllers)

if __name__ == '__main__':
    cli()
