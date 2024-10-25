import os
from flask import Blueprint
import click
from app.preservation.tools.indentifiers.fileformat import FormatIdentifier
from app.preservation.tools.validators.xmlval import validate_xml
from app.preservation.tools.validators.csvval import validate_csv
from app.preservation.tools.validators.fileformat import validate_file_format
from app.preservation.tools.validators.filename import validate_filename

bp = Blueprint('preservation_cli', __name__, cli_group=None)
# Preservation CLI group
@bp.cli.group()
def preservation():
    """Digital preservation commands."""
    pass

@preservation.command()
@click.argument('csv_file')
@click.argument('column_number', type=int)
@click.option('--delimiter', default=',', help='CSV delimiter (default is comma).')
@click.option('--encoding', default=None, help='File encoding (default is auto-detect).')
def validate_csv_command(csv_file, column_number, delimiter, encoding):
    """Validate a CSV file for the correct number of columns."""
    if not os.path.exists(csv_file):
        raise click.BadParameter(f"CSV file {csv_file} does not exist.")

    errors = validate_csv(csv_file, column_number, delimiter, encoding)

    if errors:
        click.echo(f"CSV validation failed with {len(errors)} error(s):")
        for error in errors:
            click.echo(error)
    else:
        click.echo("CSV validation successful!")


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


@preservation.command()
@click.argument('xml_file')
@click.argument('xsd_file')
def validate_xml_command(xml_file, xsd_file):
    """Validate an XML file against an XSD schema."""
    if not os.path.exists(xml_file):
        raise click.BadParameter(f"XML file {xml_file} does not exist.")

    if not os.path.exists(xsd_file):
        raise click.BadParameter(f"XSD schema file {xsd_file} does not exist.")

    result, message = validate_xml(xml_file, xsd_file)

    if result:
        click.echo("XML validation successful!")
        click.echo(message)
    else:
        click.echo("XML validation failed.")
        click.echo(message)

@preservation.command()
@click.argument('filename')
@click.argument('expected_puid')
def validate_file_format_command(filename, expected_puid):
    """Validate if the file matches the expected PUID."""


    if not os.path.exists(filename):
        raise click.BadParameter(f"File {filename} does not exist.")

    try:
        result = validate_file_format(filename, expected_puid)

        if result:
            click.echo(f"File format matches the expected PUID: {expected_puid}")
        else:
            click.echo(f"File format does not match the expected PUID: {expected_puid}")
    except Exception as e:
        click.echo(f"Error during file format validation: {str(e)}")

@preservation.command()
@click.argument('filename')
@click.option('--pattern', default=r'^[\da-zA-Z_\-]+(\.(?!([\da-zA-Z]+)\.\2)[\da-zA-Z]+)+$', help='Regex pattern to validate the filename.')
def validate_filename_command(filename, pattern):
    """Validate the given filename against a regex pattern."""
    if validate_filename(filename, pattern):
        click.echo(f"Filename '{filename}' is valid.")
    else:
        click.echo(f"Filename '{filename}' is invalid according to the pattern.")