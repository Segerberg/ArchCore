import pkg_resources
from typing import List, Tuple
import sys
import re
import psutil
import platform
import sqlite3
import os


def bytes_to_human_readable(byte_value: int) -> str:
    """
    Convert bytes to a human-readable format (KB, MB, GB, TB).

    Args:
        byte_value (int): The byte value to convert.

    Returns:
        str: The human-readable string representation of the byte value.
    """
    if byte_value < 1024:
        return f"{byte_value} B"
    elif byte_value < 1024 ** 2:
        return f"{byte_value // 1024} KB"
    elif byte_value < 1024 ** 3:
        return f"{byte_value // (1024 ** 2)} MB"
    elif byte_value < 1024 ** 4:
        return f"{byte_value // (1024 ** 3)} GB"
    elif byte_value < 1024 ** 5:
        return f"{byte_value // (1024 ** 4)} TB"
    else:
        return f"{byte_value // (1024 ** 5)} PB"



def list_installed_packages() -> List[Tuple[str, str]]:
    """
    Return a list of installed Python packages with their versions.

    Uses the pkg_resources module to retrieve a list of installed packages
    along with their versions, and returns them as a sorted list of tuples
    containing package names and versions.

    Returns:
        List[Tuple[str, str]]: A sorted list of tuples containing (package name, version).
    """
    # Get a list of all distributions (installed packages) along with versions
    installed_packages: List[Tuple[str, str]] = [(pkg.key, pkg.version) for pkg in pkg_resources.working_set]

    # Sort the list of tuples based on package names
    installed_packages.sort(key=lambda x: x[0])

    return installed_packages


def get_python_version() -> str:
    """
    Return the Python version as a string in the format 'X.Y.Z'.

    Returns:
        str: A string representing the Python version in 'X.Y.Z' format.
    """
    # Regular expression pattern to extract the version in 'X.Y.Z' format
    pattern = r'(\d+\.\d+\.\d+)'

    # Search for the pattern in the sys.version string
    match = re.search(pattern, sys.version)

    # Return the extracted version if found, otherwise return 'Unknown'
    return match.group(1) if match else 'Unknown'


def get_disk_usage(path: str) -> dict:
    """
    Return disk usage statistics of the system.

    Returns:
        dict: A dictionary containing disk usage statistics including total, used, and free space in bytes.
    """
    disk_usage = psutil.disk_usage(path)
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free
    }


def get_ram_usage() -> dict:
    """
    Return total available and used RAM statistics of the system.

    Returns:
        dict: A dictionary containing 'total' and 'used' RAM in bytes.
    """
    # Get RAM usage statistics using psutil.virtual_memory()
    ram = psutil.virtual_memory()

    return {
        'total': ram.total,
        'used': ram.used,
    }


def get_cpu_usage() -> float:
    """
    Return the current CPU usage percentage.

    Returns:
        float: CPU usage percentage.
    """
    # Get CPU usage percentage using psutil.cpu_percent()
    cpu_usage = psutil.cpu_percent(interval=1)  # Using an interval of 1 second for sampling

    return cpu_usage

def get_os_and_version() -> str:
    """
    Get the operating system name and version.

    Returns:
        str: A string containing the operating system name and version.
    """
    os_name = platform.system()  # Get the operating system name (e.g., 'Windows', 'Linux', 'Darwin')
    os_version = platform.release()  # Get the operating system version (e.g., '10.0.19041' for Windows)

    return f"{os_name} {os_version}"


def get_sqlite_version() -> str:
    """
    Get the SQLite version installed on the system.

    Returns:
        str: A string containing the SQLite version.
    """
    return sqlite3.sqlite_version


def get_cpu_info() -> dict:
    """
    Get CPU-related information.

    Returns:
        dict: A dictionary containing CPU information.
    """
    cpu_info = {}

    # Get the number of CPU cores
    cpu_info['cpu_cores'] = os.cpu_count()

    # Get the system architecture
    cpu_info['system_architecture'] = platform.architecture()[0]

    # Get the machine's processor name
    if platform.system() == 'Linux':
        with open('/proc/cpuinfo', 'r') as f:
            for line in f.readlines():
                if 'model name' in line:
                    cpu_info['processor_name'] = line.split(':')[1].strip()
                    break
    elif platform.system() == 'Darwin':  # macOS
        cpu_info['processor_name'] = platform.processor()
    elif platform.system() == 'Windows':
        cpu_info['processor_name'] = platform.processor()

    return cpu_info
