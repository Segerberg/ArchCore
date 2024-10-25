from lxml import etree
from datetime import datetime
from typing import Union


def extract_year(date: Union[datetime, str]) -> Union[int, str]:
    """
    Extracts the year from a `datetime` object or a date string in the format '%Y-%m-%d %H:%M:%S'.

    Args:
        date (Union[datetime, str]): The input can either be a `datetime` object or a date string.

    Returns:
        Union[int, str]: The year as an integer if the input is valid, or an empty string if the input is invalid.

    Example:
        >>> extract_year(datetime(2023, 10, 23))
        2023
        >>> extract_year('2023-10-23 12:34:56')
        2023
        >>> extract_year('invalid date')
        ''

    Notes:
        - If the input is a `datetime` object, the function returns the year directly.
        - If the input is a string, the function tries to parse it using the format '%Y-%m-%d %H:%M:%S'. If parsing fails, an empty string is returned.

    """
    if isinstance(date, datetime):
        return date.year
    elif isinstance(date, str):
        try:
            # Try parsing the string to a datetime object
            parsed_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return parsed_date.year
        except ValueError:
            return ''  # Return empty if it doesn't match the expected format
    return ''


def xslt_transform(xml_str: str, xslt_str: str) -> str:
    """
    Transforms an XML string using an XSLT stylesheet string and returns the resulting HTML.

    Args:
        xml_str (str): The XML content as a string.
        xslt_str (str): The XSLT stylesheet as a string.

    Returns:
        str: The transformed XML content as an HTML string.

    Raises:
        etree.XMLSyntaxError: If the XML or XSLT strings are not well-formed.
        etree.XSLTParseError: If there is an issue parsing the XSLT string.
        etree.XSLTApplyError: If the transformation fails.

    Example:
        >>> xml_data = '<greeting><name>World</name></greeting>'
        >>> xslt_data = '''
        ... <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
        ...   <xsl:template match="/">
        ...     <html><body><h1>Hello, <xsl:value-of select="greeting/name"/>!</h1></body></html>
        ...   </xsl:template>
        ... </xsl:stylesheet>
        ... '''
        >>> xslt_transform(xml_data, xslt_data)
        '<html><body><h1>Hello, World!</h1></body></html>'

        In template use:
        {{ xml_data|xslt_transform(xslt_data)|safe }}
    """
    # Parse the XML string
    xml = etree.fromstring(xml_str)

    # Parse the XSLT string
    xslt = etree.XML(xslt_str)

    # Create the transformation object
    transform = etree.XSLT(xslt)

    # Apply the transformation and return the result as a string
    result = transform(xml)

    return str(result)