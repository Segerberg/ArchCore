from app.preservation.tools.indentifiers.fileformat import FormatIdentifier
import os

def validate_file_format(filename: str, expected_puid: str) -> bool:
    """
    Validates if the file matches the expected PUID.

    Args:
        filename (str): The path to the file whose format is to be identified.
        expected_puid (str): The PUID to validate against.

    Returns:
        bool: True if the file matches the expected PUID, False otherwise.
    """

    identifier = FormatIdentifier()
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")

    format_name, format_version, format_registry_key = identifier.identify_file_format(filename)

    if format_registry_key is None:
        raise ValueError(f"Could not identify the format of the file: {filename}")

    return format_registry_key == expected_puid

