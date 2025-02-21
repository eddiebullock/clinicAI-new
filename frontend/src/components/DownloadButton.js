import React from "react";
import { Button } from "@mui/material";
import { saveAs } from "file-saver";
import { Document, Packer, Paragraph, HeadingLevel } from "docx";

function DownloadButton({ report }) {
  const handleDownload = () => {
    if (!Array.isArray(report) || report.length === 0) {
      alert("No report available to download.");
      return;
    }

    // Create a new Word document
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: report.map((section) => [
            new Paragraph({
              text: section.title,
              heading: HeadingLevel.HEADING_1,
            }),
            new Paragraph({
              text: section.content,
            }),
          ]).flat(), // Flatten the array to avoid nested arrays
        },
      ],
    });

    // Generate the .docx file and trigger download
    Packer.toBlob(doc).then((blob) => {
      saveAs(blob, "Psychological_Assessment_Report.docx");
    });
  };

  return (
    <Button
      variant="contained"
      color="secondary"
      sx={{ mt: 2 }}
      onClick={handleDownload}
    >
      Download as Word Document
    </Button>
  );
}

export default DownloadButton;
