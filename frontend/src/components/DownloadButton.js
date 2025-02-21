import React from "react";
import { Button } from "@mui/material";
import { saveAs } from "file-saver";
import { Document, Packer, Paragraph } from "docx";

function DownloadButton({ report }) {
  const handleDownload = () => {
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: [new Paragraph(report)],
        },
      ],
    });

    Packer.toBlob(doc).then((blob) => {
      saveAs(blob, "ADHD_Assessment_Report.docx");
    });
  };

  return (
    <Button variant="contained" color="secondary" sx={{ mt: 2 }} onClick={handleDownload}>
      Download as Word Document
    </Button>
  );
}

export default DownloadButton;
