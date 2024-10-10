import os
from flask import Blueprint
import click
from app.preservation.tools.indentifiers.fileformat import FormatIdentifier

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


# Preservation CLI group
@bp.cli.group()
def preservation():
    """Digital preservation commands."""
    pass

# Add the identify-format command under the preservation group
@preservation.command()
@click.argument('filename')
@click.option('--use-pronom', default=True, help='Use PRONOM formats for identification')
@click.option('--use-extension', default=True, help='Use extension-based formats for identification')
def identify_format(filename, use_pronom, use_extension):
    """Identify the format of a given file using FIDO"""
    if not os.path.exists(filename):
        raise click.BadParameter(f"File {filename} does not exist.")

    identifier = FormatIdentifier(
        use_fido_pronom_formats=use_pronom,
        use_fido_extension_formats=use_extension
    )

    try:
        format_name, format_version, format_registry_key = identifier.identify_file_format(filename)

        if format_name:
            click.echo(f"Format Name: {format_name}")
            click.echo(f"Format Version: {format_version if format_version else 'N/A'}")
            click.echo(f"Format Registry Key (PUID): {format_registry_key if format_registry_key else 'N/A'}")
        else:
            click.echo("Unknown file format.")
    except Exception as e:
        raise click.ClickException(f"Error identifying file format: {str(e)}")



@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

