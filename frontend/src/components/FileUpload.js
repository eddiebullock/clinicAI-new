import React, { useState } from "react";
import { Button, Box, Typography } from "@mui/material";
import { uploadTranscript } from "../api";

function FileUpload({ setReport }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }
    
    setLoading(true);
    
    try {
      const report = await uploadTranscript(selectedFile);
      setReport(report);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to generate report. Please try again.");
    }

    setLoading(false);
  };

  return (
    <Box sx={{ mt: 3, textAlign: "center" }}>
      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
        style={{ display: "none" }}
        id="file-upload"
      />
      <label htmlFor="file-upload">
        <Button variant="contained" component="span">
          Select Transcript File
        </Button>
      </label>

      {selectedFile && (
        <Typography sx={{ mt: 2 }}>{selectedFile.name}</Typography>
      )}

      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Processing..." : "Generate Report"}
      </Button>
    </Box>
  );
}

export default FileUpload;
