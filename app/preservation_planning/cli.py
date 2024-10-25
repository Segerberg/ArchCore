import os
import click
from flask import Blueprint
from app.preservation_planning.tools.registry.importer import import_pp_file
bp = Blueprint('preservation_planning_cli', __name__, cli_group=None)
@bp.cli.group()
def preservation_planning():
    """Preservation planning commands."""
    pass

@preservation_planning.command()
@click.argument('csv_file')
def import_pp_registry(csv_file):
    """Import preservation planning registry list from a CSV file """
    if not os.path.exists(csv_file):
        raise click.BadParameter(f"CSV file {csv_file} does not exist.")
    import_pp_file(csv_file)
