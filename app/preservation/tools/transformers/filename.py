import os
import string
import unicodedata

DEFAULT_WHITELIST_FILE = "-_. %s%s" % (string.ascii_letters, string.digits)
DEFAULT_WHITELIST_DIR = "-_ %s%s" % (string.ascii_letters, string.digits)

def transform_filename(path: str, whitelist: str = None, replace: dict = None, normalize_unicode: bool = True) -> None:
    """
    Transforms the file or directory name by replacing certain characters, optionally normalizing Unicode,
    and ensuring the name only contains whitelisted characters.

    Args:
        path (str): The original file or directory path.
        whitelist (str, optional): A string of allowed characters. If None, a default whitelist is used:
            - For files: "-_. <letters><digits>"
            - For directories: "-_ <letters><digits>"
        replace (dict, optional): A dictionary specifying character replacements (e.g., {' ': '_'}).
            If None, defaults to replacing spaces with underscores.
            For directories, dots are also replaced with underscores by default.
        normalize_unicode (bool, optional): If True, normalizes the filename to ASCII, removing any special characters.
            Defaults to True.

    Returns:
        None: The function renames the file or directory with the transformed name.

    Example:
        Given a file path 'my archive.tar.gz', the function can rename it to 'my_archive.tar.gz',
        ensuring it only contains whitelisted characters and optional Unicode normalization.

    Behavior:
        - For files: Allows dots (.) but replaces spaces with underscores.
        - For directories: Replaces dots with underscores and spaces with underscores.
        - Optionally strips non-ASCII characters if `normalize_unicode` is enabled.

    Raises:
        OSError: If the file or directory cannot be renamed.
    """
    # Determine whitelist based on whether path is a file or directory
    if whitelist is None:
        whitelist = DEFAULT_WHITELIST_FILE if os.path.isfile(path) else DEFAULT_WHITELIST_DIR

    # Default replacements: spaces to underscores, and optionally dots to underscores for directories
    if replace is None:
        replace = {' ': '_'}
        if os.path.isdir(path):
            replace['.'] = '_'

    # Get the base name of the file/directory
    basename = os.path.basename(path)

    # Apply replacements
    for k, v in replace.items():
        basename = basename.replace(k, v)

    # Normalize Unicode if enabled
    if normalize_unicode:
        basename = unicodedata.normalize('NFKD', basename).encode('ASCII', 'ignore').decode()

    # Keep only whitelisted characters
    new_basename = ''.join(c for c in basename if c in whitelist)

    # Rename the file or directory with the cleaned name
    os.rename(path, os.path.join(os.path.dirname(path), new_basename))