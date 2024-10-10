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