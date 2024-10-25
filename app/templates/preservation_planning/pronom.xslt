<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:pronom="http://pronom.nationalarchives.gov.uk"
                exclude-result-prefixes="pronom">

  <!-- Output as HTML -->
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <!-- Template that matches the root element -->
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title>PRONOM Report</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
          }
          h1, h2, h3 {
            color: #333;
          }
          .section {
            margin-bottom: 20px;
          }
          .label {
            font-weight: bold;
            color: #0056b3;
          }
          .value {
            margin-left: 10px;
          }
          .related-formats {
            margin-left: 20px;
          }
          summary {
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
          }
        </style>
      </head>
      <body>
        <h1>PRONOM Report</h1>

        <!-- Apply templates to the report details -->
        <xsl:apply-templates select="//pronom:report_format_detail/pronom:FileFormat"/>

      </body>
    </html>
  </xsl:template>

  <!-- Template to handle FileFormat details -->
  <xsl:template match="pronom:FileFormat">
    <div class="section">
      <details open="true">
        <summary>Format Details</summary>
        <div>
          <div class="label">Format ID:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatID"/>
          </div>

          <div class="label">Format Name:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatName"/>
          </div>

          <div class="label">Format Version:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatVersion"/>
          </div>

          <div class="label">Format Aliases:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatAliases"/>
          </div>

          <div class="label">Format Types:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatTypes"/>
          </div>

          <div class="label">Format Disclosure:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatDisclosure"/>
          </div>

          <div class="label">Format Description:</div>
          <div class="value">
            <xsl:value-of select="pronom:FormatDescription"/>
          </div>

          <div class="label">Binary File Format:</div>
          <div class="value">
            <xsl:value-of select="pronom:BinaryFileFormat"/>
          </div>

          <div class="label">Byte Orders:</div>
          <div class="value">
            <xsl:value-of select="pronom:ByteOrders"/>
          </div>

          <div class="label">Last Updated Date:</div>
          <div class="value">
            <xsl:value-of select="pronom:LastUpdatedDate"/>
          </div>
        </div>
      </details>
    </div>

    <!-- Handling FileFormatIdentifiers -->
    <div class="section">
      <details>
        <summary>File Format Identifiers</summary>
        <xsl:for-each select="pronom:FileFormatIdentifier">
          <div>
            <span class="label">Identifier Type:</span>
            <span class="value"><xsl:value-of select="pronom:IdentifierType"/></span>
            <br/>
            <span class="label">Identifier:</span>
            <span class="value"><xsl:value-of select="pronom:Identifier"/></span>
          </div>
        </xsl:for-each>
      </details>
    </div>

    <!-- Handling Developers -->
    <div class="section">
      <details>
        <summary>Developer Information</summary>
        <div>
          <span class="label">Organisation Name:</span>
          <span class="value"><xsl:value-of select="pronom:Developers/pronom:OrganisationName"/></span>
        </div>
      </details>
    </div>

    <!-- Handling External Signatures -->
    <div class="section">
      <details>
        <summary>External Signatures</summary>
        <xsl:for-each select="pronom:ExternalSignature">
          <div>
            <span class="label">Signature:</span>
            <span class="value"><xsl:value-of select="pronom:Signature"/></span>
            <br/>
            <span class="label">Signature Type:</span>
            <span class="value"><xsl:value-of select="pronom:SignatureType"/></span>
          </div>
        </xsl:for-each>
      </details>
    </div>

    <!-- Handling Related Formats -->
    <div class="section">
      <details>
        <summary>Related Formats</summary>
        <xsl:for-each select="pronom:RelatedFormat">
          <div class="related-formats">
            <span class="label">Relationship:</span>
            <span class="value"><xsl:value-of select="pronom:RelationshipType"/></span>
            <br/>
            <span class="label">Related Format Name:</span>
            <span class="value"><xsl:value-of select="pronom:RelatedFormatName"/></span>
            <br/>
            <span class="label">Related Format Version:</span>
            <span class="value"><xsl:value-of select="pronom:RelatedFormatVersion"/></span>
          </div>
        </xsl:for-each>
      </details>
    </div>

  </xsl:template>

</xsl:stylesheet>