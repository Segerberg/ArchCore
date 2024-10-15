from lxml import etree

def validate_xml(xml_file: str, xsd_file: str) -> tuple[bool, str]:
    """
    Validate an XML file against a given XML Schema (XSD).

    Args:
        xml_file (str): Path to the XML file.
        xsd_file (str): Path to the XSD schema file.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether
                          the XML is valid, and a string with validation
                          messages or errors.
    """
    try:
        # Parse the XSD file
        with open(xsd_file, 'rb') as schema_file:
            schema_doc = etree.parse(schema_file)
            xml_schema = etree.XMLSchema(schema_doc)

        # Parse the XML file
        with open(xml_file, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)

        # Validate the XML file against the schema
        xml_schema.assertValid(xml_doc)
        return True, "XML is valid."

    except (etree.XMLSchemaError, etree.DocumentInvalid) as e:
        return False, str(e)
    except Exception as e:
        return False, f"An error occurred: {str(e)}"