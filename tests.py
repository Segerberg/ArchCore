import unittest
import re
import sys
from app.main.utils import (
bytes_to_human_readable,
list_installed_packages,
get_python_version,
get_disk_usage
)


class TestBytesToHumanReadable(unittest.TestCase):
    """
    A test case class for validating the bytes_to_human_readable function.

    This class contains unit tests to verify the functionality
    of the bytes_to_human_readable function, ensuring that it
    correctly converts byte values into human-readable formats
    such as KB, MB, GB, TB, and PB.
    """

    def test_bytes_to_human_readable(self):
        """
        Test the bytes_to_human_readable function with various input values.

        This method iterates through a dictionary of test cases and uses
        the assertEqual method to compare the output of the bytes_to_human_readable
        function with the expected human-readable representation for each byte value.
        """
        test_cases = {
            0: "0 B",
            1023: "1023 B",
            1024: "1 KB",
            1024 ** 2: "1 MB",
            1024 ** 3: "1 GB",
            1024 ** 4: "1 TB",
            1024 ** 5: "1 PB",
            1024 ** 6: "1024 PB"
        }

        for byte_value, expected_output in test_cases.items():
            with self.subTest(byte_value=byte_value):
                self.assertEqual(bytes_to_human_readable(byte_value), expected_output)

class TestListInstalledPackages(unittest.TestCase):
    """
    A unit test class to verify the functionality of the list_installed_packages function.
    """

    def test_list_installed_packages(self):
        """
        Test the list_installed_packages function to ensure it returns a list of tuples
        containing package names and versions.
        """
        # Call the function to get the list of installed packages
        packages = list_installed_packages()

        # Verify that the returned value is a list
        self.assertIsInstance(packages, list)

        # Verify that each item in the list is a tuple containing two elements
        for package_info in packages:
            with self.subTest(package_info=package_info):
                self.assertIsInstance(package_info, tuple)
                self.assertEqual(len(package_info), 2)

                # Verify that the first and second elements of the tuple are strings
                self.assertIsInstance(package_info[0], str)
                self.assertIsInstance(package_info[1], str)


class TestGetPythonVersion(unittest.TestCase):
    """
    A unit test class to verify the functionality of the get_python_version function.
    """

    def test_get_python_version_format(self):
        """
        Test the get_python_version function to ensure it returns a version string in 'X.Y.Z' format.
        """
        python_version = get_python_version()

        # Verify that the returned version string matches the 'X.Y.Z' pattern
        pattern = r'^\d+\.\d+\.\d+$'
        self.assertTrue(re.match(pattern, python_version),
                        f"The returned version '{python_version}' does not match the 'X.Y.Z' format.")


class TestGetDiskUsage(unittest.TestCase):
    """
    A unit test class to verify the functionality of the get_disk_usage function.
    """

    def test_get_disk_usage(self):
        """
        Test the get_disk_usage function to ensure it returns a dictionary with valid disk usage statistics.
        """
        disk_usage_stats = get_disk_usage()

        # Verify that the returned value is a dictionary
        self.assertIsInstance(disk_usage_stats, dict)

        # Verify that the dictionary contains expected keys
        self.assertIn('total', disk_usage_stats)
        self.assertIn('used', disk_usage_stats)
        self.assertIn('free', disk_usage_stats)

        # Verify that the values associated with each key are positive integers
        for key in ['total', 'used', 'free']:
            with self.subTest(key=key):
                self.assertIsInstance(disk_usage_stats[key], int)
                self.assertGreaterEqual(disk_usage_stats[key], 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)