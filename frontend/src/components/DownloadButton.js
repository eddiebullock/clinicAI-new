// DownloadButton.js
import React from "react";
import { Button } from "@mui/material";

const DownloadButton = ({ content }) => {
  const handleDownload = () => {
    const blob = new Blob([content], { type: "text/html" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "assessment_report.html";
    link.click();
  };

  return (
    <Button variant="contained" color="primary" onClick={handleDownload}>
      Download Edited Report
    </Button>
  );
};

export default DownloadButton;