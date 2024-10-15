import re

def validate_filename(filename: str, pattern: str = r'^[\da-zA-Z_\-]+(\.(?!([\da-zA-Z]+)\.\2)[\da-zA-Z]+)+$') -> bool:
    """
    Validates the given filename against the specified regex pattern.

    Args:
        filename (str): The filename to validate.
        pattern (str): The regex pattern to use for validation.

    Returns:
        bool: True if the filename matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, filename))

