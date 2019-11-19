import click

from .invalidate import invalidate
from .run import run


@click.group()
def main():
    pass


main.add_command(run)
main.add_command(invalidate)
