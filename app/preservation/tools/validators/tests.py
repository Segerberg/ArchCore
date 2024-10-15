import unittest
import os
from app.preservation.tools.validators.xmlval import validate_xml  # Import the function from your module

class TestXMLValidation(unittest.TestCase):

    def setUp(self):
        # Create temporary XSD and XML files for testing
        self.valid_xsd = 'valid_schema.xsd'
        self.valid_xml = 'valid_xml.xml'
        self.invalid_xml = 'invalid_xml.xml'

        # Writing a simple valid schema
        with open(self.valid_xsd, 'w') as xsd_file:
            xsd_file.write('''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="note">
                                  <xs:complexType>
                                    <xs:sequence>
                                      <xs:element name="to" type="xs:string"/>
                                      <xs:element name="from" type="xs:string"/>
                                      <xs:element name="heading" type="xs:string"/>
                                      <xs:element name="body" type="xs:string"/>
                                    </xs:sequence>
                                  </xs:complexType>
                                </xs:element>
                              </xs:schema>''')

        # Writing a valid XML file
        with open(self.valid_xml, 'w') as xml_file:
            xml_file.write('''<note>
                                <to>Tove</to>
                                <from>Jani</from>
                                <heading>Reminder</heading>
                                <body>Don't forget me this weekend!</body>
                              </note>''')

        # Writing an invalid XML file (missing a required element)
        with open(self.invalid_xml, 'w') as xml_file:
            xml_file.write('''<note>
                                <to>Tove</to>
                                <from>Jani</from>
                                <heading>Reminder</heading>
                              </note>''')  # Missing <body> element

    def tearDown(self):
        # Cleanup temporary files
        os.remove(self.valid_xsd)
        os.remove(self.valid_xml)
        os.remove(self.invalid_xml)

    def test_valid_xml(self):
        """Test that a valid XML file passes validation."""
        result, message = validate_xml(self.valid_xml, self.valid_xsd)
        self.assertTrue(result)
        self.assertEqual(message, "XML is valid.")

    def test_invalid_xml(self):
        """Test that an invalid XML file fails validation."""
        result, message = validate_xml(self.invalid_xml, self.valid_xsd)
        self.assertFalse(result)
        self.assertIn("Element 'note': Missing child element", message)

    def test_nonexistent_files(self):
        """Test that the function handles non-existent files gracefully."""
        result, message = validate_xml('nonexistent.xml', 'nonexistent.xsd')
        self.assertFalse(result)
        self.assertIn("An error occurred", message)

if __name__ == '__main__':
    unittest.main()