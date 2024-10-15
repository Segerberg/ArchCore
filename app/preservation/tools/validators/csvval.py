import csv
from typing import List


def validate_csv(path: str, column_number: int, delimiter: str = ',', encoding: str = None) -> List[str]:
    """
    Validates a CSV file by checking if each row has the correct number of columns and if every row ends with a newline character.

    Args:
        path (str): The file path to the CSV file.
        column_number (int): The expected number of columns in each row.
        delimiter (str, optional): The delimiter used in the CSV file. Defaults to ','.
        encoding (str, optional): The encoding of the CSV file. If None, the system's default encoding is used.

    Returns:
        List[str]: A list of error messages. Each error message indicates a row with an incorrect number of columns or missing newline characters.

    Example:
        Given a CSV file `data.csv` with 3 columns expected:

        ```python
        errors = validate_csv('data.csv', 3)
        if errors:
            for error in errors:
                print(error)
        ```

    Behavior:
        - **Line break validation**: Checks if each line ends with a newline character (`\n`).
        - **Column validation**: Ensures each row has the specified number of columns (`column_number`).
        - **CSV parsing**: Uses Python’s built-in `csv.reader` to handle CSV structure based on the specified `delimiter` and `quotechar`.

    Error Handling:
        - Rows with an incorrect number of columns will generate an error message in the format:
          `"Wrong number of columns for row {row}"`
        - Rows missing a newline character at the end will generate an error message in the format:
          `"Missing line break for post {row}"`

    Raises:
        OSError: If the file cannot be opened.
        UnicodeDecodeError: If there is a problem with the file encoding.
    """
    errors = []

    # Check for missing newline characters in each row
    with open(path, 'r', encoding=encoding) as csvfile:
        for row in csvfile:
            if not row.endswith('\n'):
                msg = f'Missing line break for post {row}'
                errors.append(msg)

        # Reset file pointer to the beginning
        csvfile.seek(0)

        # Use CSV reader to check for column consistency
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')

        # Validate the number of columns in each row
        for row in reader:
            if len(row) != column_number:
                msg = f'Wrong number of columns for row {row}'
                errors.append(msg)

    return errors