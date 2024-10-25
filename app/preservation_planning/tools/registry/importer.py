import csv
import zipfile
from typing import Union
from lxml import etree
from fido import CONFIG_DIR
from fido.versions import get_local_versions
from app import db
from app.models import FormatRegistry

# Get the local signature file and zip file
versions = get_local_versions(CONFIG_DIR)
signature_file = versions.get_signature_file()
signature_zip = versions.get_zip_file()


class InvalidFormatError(Exception):
    """Custom exception raised when an invalid file format is encountered."""

    def __init__(self, message: str = "Invalid file format detected") -> None:
        self.message = message
        super().__init__(self.message)


def import_pp_file(file: Union[str, bytes]) -> None:
    """
    Imports a CSV file with preservation action details and updates the database.

    Args:
        file (Union[str, bytes]): The path to the CSV file or a file-like object.

    Raises:
        InvalidFormatError: If the CSV file has an incorrect format or structure.
        KeyError: If a PUID is not found in the signature ZIP file.

    The function processes the CSV, looks up the corresponding XML signature file for each PUID
    from the signature ZIP, and adds entries to the database for each valid row in the CSV.
    """
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

        # Check for valid header structure
        if len(header) != 4:
            raise InvalidFormatError("CSV file must have exactly 4 columns")
        if 'fmt' in header[0]:
            raise InvalidFormatError("Invalid header format: 'fmt' found in the first column")

        # Process each row in the CSV
        for puid, preservation, allowed, action in reader:
            sig_zip = zipfile.ZipFile(signature_zip, 'r')
            sig_filename = f"puid.{puid.replace('/', '.')}.xml"

            try:
                # Extract and parse the XML from the signature ZIP file
                pronom_xml = sig_zip.read(sig_filename)
                ns = {'ns': 'http://pronom.nationalarchives.gov.uk'}
                root = etree.fromstring(pronom_xml)

                # Find format name and version from the XML
                format_name = root.find('.//ns:FormatName', namespaces=ns).text
                format_version = root.find('.//ns:FormatVersion', namespaces=ns).text

                # Create a new FormatRegistry entry
                format_registry = FormatRegistry(
                    puid=puid,
                    format_name=format_name,
                    format_version=format_version,
                    pronom_xml=pronom_xml,
                    preservation=bool(preservation),
                    allowed=bool(allowed),
                    action=action
                )
                db.session.add(format_registry)
            except KeyError:
                # Raise an error if the PUID file is not found in the signature ZIP
                raise KeyError(f"PUID '{puid}' not found in the signature ZIP file")

    # Commit the session to save all entries
    db.session.commit()

