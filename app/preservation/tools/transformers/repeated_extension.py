import os
import re
from typing import Tuple

# Regex pattern to identify repeated file extensions (e.g., .tar.gz.gz)
REPEATED_PATTERN = r'\.(\w+)(\.(\1))+'


def transform_repeated_extension(path: str) -> Tuple[str, os]:
    """
    Transforms file paths by removing repeated file extensions and renaming the file.

    Args:
        path (str): The original file path.

    Returns:
        Tuple[str, os]:
            - str: The new file name (without directory).
            - os: The os module for potential further use.

    Example:
        Given a path like 'archive.tar.gz.gz', it renames the file to 'archive.tar.gz'.
    """
    # Replace repeated extensions with a single occurrence (e.g., .gz.gz -> .gz)
    new_path = re.sub(REPEATED_PATTERN, '.\\1', path)

    # Rename the file with the transformed path
    os.rename(path, new_path)

    return os.path.basename(path), os.path.basename(new_path)
