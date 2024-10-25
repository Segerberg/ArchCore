# File Format Identification
ArchCore utilizes FIDO (Format Identification for Digital Objects) as a key component in identifying the file formats.

FIDO is a tool developed by the Open Preservation Foundation that analyzes digital objects to determine their file formats.
It's designed to integrate seamlessly into automated workflows, making it ideal for large-scale digital preservation operations. 
FIDO achieves its identification capabilities by leveraging the UK National Archives' PRONOM File Format and Container descriptions.

FIDO employs two primary methods for identifying file formats:
* Signature Analysis: FIDO examines the internal structure of a file, looking for specific byte sequences (signatures) that uniquely identify a particular format This method provides high accuracy and reliability.

* File Extension Matching: As a secondary method, FIDO can also identify formats based on the file extension (e.g., .docx, .pdf) This method is less reliable than signature analysis, as file extensions can be easily changed, but it can still provide useful information.

FIDO provides detailed output about identified formats, including:
* PUID (PRONOM Unique Identifier)
* Format Name
* Version Information
* MIME Type
* Match Type (signature, extension, container)

# Validators

## Filename
The validate_filename function checks if a given filename is valid according to a specified regular expression (regex) 
pattern. By default, it ensures that the filename consists of alphanumeric characters, underscores (_), hyphens (-), 
and can include valid extensions. The function also prevents multiple consecutive extensions from being the same.

### Parameters
* filename (str): The filename to validate. 
* pattern (str, optional): The regular expression pattern used for validation. The default pattern ensures that the filename:
	•Contains alphanumeric characters (a-z, A-Z, 0-9), underscores (_), or hyphens (-).
	•Includes one or more valid extensions (e.g., .txt, .pdf, .jpg).
	•Disallows consecutive identical extensions (e.g., .tar.tar is invalid).

# XML
The validate_xml function checks whether an XML file conforms to the structure and rules defined by a 
provided XML Schema Definition (XSD) file. It parses both the XML and XSD files, and returns the validation 
status along with any error messages.

### Parameters

* xml_file (str): Path to the XML file to be validated.
* xsd_file (str): Path to the XSD file used for validation.
