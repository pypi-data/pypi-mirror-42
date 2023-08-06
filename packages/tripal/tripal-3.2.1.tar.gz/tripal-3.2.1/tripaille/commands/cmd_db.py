import click
from tripaille.commands.db.get_dbs import cli as func0
from tripaille.commands.db.get_mviews import cli as func1
from tripaille.commands.db.index import cli as func2
from tripaille.commands.db.populate_mviews import cli as func3
from tripaille.commands.db.tune import cli as func4


@click.group()
def cli():
    """Access Tripal/Chado database"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
